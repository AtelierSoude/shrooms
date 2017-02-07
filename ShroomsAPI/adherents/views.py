from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_extensions.mixins import NestedViewSetMixin
from adherents.models import Adherent, Subscription, SubscriptionType
from adherents.serializers import (ProfileSubscriptionSerializer,
                                   SubscribeSerializer, SubscriptionSerializer,
                                   SubscriptionTypeSerializer)
from django.contrib.auth import get_user_model

USERNAME_FIELD = get_user_model().USERNAME_FIELD

"""
API views
"""

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

    @list_route()
    def active(self, request):
        active_sub = Subscription.objects.active()
        page = self.paginate_queryset(active_sub)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active_sub, many=True)
        return Response(serializer.data)
