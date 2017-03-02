from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SlugRelatedField
)

from profiles.models import (
    UserProfile,
    Organisation,
    BaseGroup,
    OrganisationGroup,
    OrganisationType
)

from users.serializers import UserSerializer, UserShortSerializer

from django.conf import settings

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

class UserProfileShortSerializer(HyperlinkedModelSerializer):
    """
    Short serializer for user profile
    """
    user = UserShortSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'url',
            'pk',
            'user',
            'first_name',
            'last_name',
            'about',
            'website',
        ]
        extra_kwargs = {
            'url': {'view_name': 'userprofile-detail'},
        }
        read_only_fields = ('pk', 'user',)


class UserProfileSerializer(HyperlinkedModelSerializer):
    """
    Serializer for user profile
    """
    user = UserShortSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'url',
            'pk',
            'user',
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'groups',
            'phone_number',
            'newsletter_subscription',
            'date_created',
            'about',
            'website',
        ]
        extra_kwargs = {
            'url': {'view_name': 'userprofile-detail'},
            'groups': {'view_name': 'basegroup-detail'},
        }
        read_only_fields = ('pk', 'user', 'date_created')

class OrganisationSerializer(HyperlinkedModelSerializer):
    """
    Organisation model serializer
    """
    type = SlugRelatedField(
        queryset=OrganisationType.objects.all(),
        slug_field='type'
    )
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
            'organisation_group'
        )
        extra_kwargs = {
            'url': {'view_name': 'organisation-detail'},
            'main_contact': {'view_name': 'userprofile-detail'},
            'organisation_group': {'view_name': 'organisationgroup-detail'},
        }


class BaseGroupSerializer(HyperlinkedModelSerializer):
    """
    Group model serializer
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
            'url': {'view_name': 'basegroup-detail'},
            'members': {'view_name': 'userprofile-detail'},
        }


class OrganisationGroupSerializer(HyperlinkedModelSerializer):
    """
    Group model serializer
    """
    class Meta:
        model = OrganisationGroup
        fields = (
            'url',
            'name',
            'description',
            'members',
            'organisation'
        )
        extra_kwargs = {
            'url': {'view_name': 'organisationgroup-detail'},
            'members': {'view_name': 'userprofile-detail'},
            'organisation': {'view_name': 'organisation-detail'},
        }

class OrganisationTypeSerializer(HyperlinkedModelSerializer):
    """
    Group model serializer
    """
    class Meta:
        model = OrganisationType
        fields = (
            'url',
            'type',
        )
        extra_kwargs = {
            'url': {'view_name': 'organisationtype-detail'},
        }
