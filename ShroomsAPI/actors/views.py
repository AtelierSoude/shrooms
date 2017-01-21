from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

from actstream import action
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from .models import (
    Individual,
    Adherent,
    Subscription,
    SubscriptionType,
    Organisation
)
# from .mixins import *
# from .forms import *
from .serializers import (
    IndividualSerializer,
    AdherentSerializer,
    SubscriptionSerializer,
    SubscriptionTypeSerializer,
    OrganisationSerializer
)


# Create your views here.

class IndividualViewSet(viewsets.ModelViewSet):
    """
    Users viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer

class AdherentViewSet(viewsets.ModelViewSet):
    """
    Users viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Adherent.objects.all()
    serializer_class = AdherentSerializer

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

class OrganisationViewSet(viewsets.ModelViewSet):
    """
    Subscription viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer