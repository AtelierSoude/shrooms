from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets

from adherents.models import Subscription, SubscriptionType
from adherents.serializers import (SubscriptionSerializer,
                                   SubscriptionTypeSerializer)


# Create your views here.


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
