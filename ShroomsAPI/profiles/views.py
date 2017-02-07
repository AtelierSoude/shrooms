#from actstream import action
from rest_framework import generics, permissions, status, viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.contrib.auth import get_user_model

from profiles.models import (
    UserProfile,
    Organisation,
    BaseGroup,
    OrganisationGroup
)
# from .mixins import *
# from .forms import *
from profiles.serializers import (
    UserProfileSerializer,
    OrganisationSerializer,
    BaseGroupSerializer,
    OrganisationGroupSerializer
)




class ProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

"""
Admin API views
"""


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Users viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


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