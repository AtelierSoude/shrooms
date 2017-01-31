#from actstream import action
from rest_framework import generics, permissions, status, viewsets


from profiles.models import (
    UserProfile,
    Organisation,
    BaseGroup,
)
# from .mixins import *
# from .forms import *
from profiles.serializers import (
    UserProfileSerializer,
    OrganisationSerializer,
    BaseGroupSerializer,
)

#
# ACTOR VIEWS
#

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
