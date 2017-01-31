from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from adherents.models import Adherent, Subscription, SubscriptionType
from adherents.serializers import (ReadOnlySubscriptionSerializer,
                                   SubscribeSerializer, SubscriptionSerializer,
                                   SubscriptionTypeSerializer)


"""
API views
"""


class SubscriptionRootView(views.APIView):
    """
    Root endpoint - use one of sub endpoints.
    """
    permission_classes = (
        permissions.AllowAny,
    )
    urls_mapping = {
        'subscribe': 'subscribe',
        'my subscriptions': 'user-subscriptions',
    }
    urls_extra_mapping = None

    def get_urls_mapping(self, **kwargs):
        mapping = self.urls_mapping.copy()
        mapping.update(kwargs)
        if self.urls_extra_mapping:
            mapping.update(self.urls_extra_mapping)
        return mapping

    def get(self, request, format=None):
        return Response(
            dict([(key, reverse(url_name, request=request, format=format))
                  for key, url_name in self.get_urls_mapping().items()])
        )


class SubscribeView(generics.CreateAPIView):
    """
    Authenticated user with valid user profile may subscribe here
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer


class UserSubscriptionViewset(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for auth users, allowing to browse their subscriptions
    """
    queryset = Subscription.objects.all()
    serializer_class = ReadOnlySubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super(UserSubscriptionViewset, self).get_queryset().filter(
            adherent=self.request.user.profile)

    @list_route(methods=['get'])
    def active_subscription(self, request):
        adherent = Adherent.objects.get(pk=self.request.user.profile.pk)
        subscription = getattr(adherent, 'active_subscription', None)
        print(adherent)
        print(subscription)
        if subscription is not None:
            serializer = ReadOnlySubscriptionSerializer(subscription)
            return Response(serializer.data)
        else:
            return Response(_('You don\'t have any currently active subscription.'), status=status.HTTP_204_NO_CONTENT)

"""
Admin viewsets
"""


class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    """
    Subscription types viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Subscription viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
