from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
)

from profiles.models import (
    UserProfile,
    Organisation,
    BaseGroup,
)

"""
FIELDS

"""


"""
SERIALIZERS

"""


"""
All fields serializers
Used for Admin API endpoints
"""

class UserProfileSerializer(HyperlinkedModelSerializer):
    """
    Serializer for user profile
    """
    class Meta:
        model = UserProfile
        fields = (
            'url',
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'user',
            'groups',
            'phone_number',
            'newsletter_subscription',
            'date_created',
            'about',
            'website',
        )
        extra_kwargs = {
            'url': {'view_name': 'admin-api:userprofile-detail'},
            'user': {'view_name': 'admin-api:user-detail'},
            'groups': {'view_name': 'admin-api:basegroup-detail'},
        }

class OrganisationSerializer(HyperlinkedModelSerializer):
    """
    Organisation model serializer
    """
    class Meta:
        model = Organisation
        fields = (
            'url',
            'short_name',
            'full_name',
            'type',
            'main_contact',
            'phone_number',
            'email',
            'date_created',
            'about',
            'website',
        )
        extra_kwargs = {
            'url': {'view_name': 'admin-api:organisation-detail'},
            'main_contact': {'view_name': 'admin-api:userprofile-detail'},
        }


class BaseGroupSerializer(HyperlinkedModelSerializer):
    """
    Organisation model serializer
    """
    class Meta:
        model = BaseGroup
        fields = (
            'url',
            'members',
            'name',
            'description',
        )
        extra_kwargs = {
            'url': {'view_name': 'admin-api:basegroup-detail'},
            'members': {'view_name': 'admin-api:userprofile-detail'},
        }