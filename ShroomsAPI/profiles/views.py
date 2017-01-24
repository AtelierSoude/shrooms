#from actstream import action
from rest_framework import generics, permissions, status, viewsets


from profiles.models import (
    UserProfile,
    Organisation
)
# from .mixins import *
# from .forms import *
from profiles.serializers import (
    UserProfileSerializer,
    OrganisationSerializer,
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




class OrganisationViewSet(viewsets.ModelViewSet):
    """
    Subscription viewset
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
