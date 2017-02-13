from adherents.models import Adherent, Subscription, SubscriptionType
from adherents.serializers import (AdherentSerializer, AdherentShortSerializer,
                                   SubscribeSerializer, SubscriptionSerializer,
                                   SubscriptionTypeSerializer)
from django.contrib.auth import get_user_model, models
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from dry_rest_permissions.generics import DRYPermissions
from profiles.views import ProfileViewSet
from profiles.mixins import AltSerializerMixin
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_extensions.mixins import NestedViewSetMixin

USERNAME_FIELD = get_user_model().USERNAME_FIELD

"""
API views
"""


class AdherentViewSet(ProfileViewSet, AltSerializerMixin):
    """
    Adherent viewset with alternative serializer to use depending
    on auth user.
    Shows only currently subscribed Profiles
    """
    queryset = Adherent.objects.active()
    permission_classes = (DRYPermissions,)
    serializer_class = AdherentShortSerializer
    alt_serializer_class = AdherentSerializer

    def retrieve(self, request, *args, **kwargs):
        "Custom retrieve method allowing alternative serializer"
        instance = self.get_object()
        if instance.user == request.user or request.user.is_staff or request.user.is_superuser:
            serializer = self.get_alt_serializer(instance)
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SubscribeView(generics.CreateAPIView):
    """
    Authenticated user with valid user profile may subscribe here
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

"""
Admin viewsets
"""


class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    """
    Subscription types viewset
    """
    permission_classes = (DRYPermissions,)
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Subscription viewset
    """
    permission_classes = (DRYPermissions,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @list_route()
    def active(self, request):
        "List currently active subscriptions"
        active_sub = Subscription.objects.active()
        page = self.paginate_queryset(active_sub)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active_sub, many=True)
        return Response(serializer.data)
