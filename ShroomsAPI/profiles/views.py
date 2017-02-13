#from actstream import action
from django.contrib.auth import get_user_model
from profiles.models import (BaseGroup, Organisation, OrganisationGroup,
                             UserProfile)
from profiles.mixins import AltSerializerMixin
# from .forms import *
from profiles.serializers import (BaseGroupSerializer,
                                  OrganisationGroupSerializer,
                                  OrganisationSerializer,
                                  UserProfileSerializer,
                                  UserProfileShortSerializer)
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin


class ProfileViewSet(AltSerializerMixin, viewsets.ModelViewSet):
    """
    Profile viewset with alternative serializer to use depending
    on auth user
    """
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileShortSerializer
    alt_serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        "Custom retrieve method allowing alternative serializer"
        instance = self.get_object()
        if instance.user == request.user or request.user.is_staff or request.user.is_superuser:
            serializer = self.get_alt_serializer(instance)
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)

    


"""
Admin API views
"""


class ProfileGroupViewSet(viewsets.ModelViewSet):
    """
    Profile groups viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = BaseGroup.objects.all()
    serializer_class = BaseGroupSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    """
    Subscription viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

class OrganisationGroupViewSet(viewsets.ModelViewSet):
    """
    Organisation group viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = OrganisationGroup.objects.all()
    serializer_class = OrganisationGroupSerializer
