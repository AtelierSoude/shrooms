from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets

from adherents.models import Subscription, SubscriptionType
from adherents.serializers import (SubscriptionSerializer,
                                   SubscriptionTypeSerializer)


# Create your views here.



class SubscribeView(generics.CreateAPIView):
    """
    Authenticated user with valid user profile may subscribe here
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


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
