from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    HyperlinkedIdentityField,
    ModelSerializer,
)

from profiles.models import (
    UserProfile,
    Organisation,
    BaseGroup,
    OrganisationGroup
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

class UserProfileSerializer(HyperlinkedModelSerializer):
    """
    Serializer for user profile
    """
    user = UserShortSerializer()
    '''if 'adherents' in settings.INSTALLED_APPS:
        subscriptions = HyperlinkedRelatedField(
            read_only=True,
            view_name = 'profile-subscription'
        )'''
    class Meta:
        NAMESPACE = ''
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
        '''if 'adherents' in settings.INSTALLED_APPS:
            fields += ['subscriptions']'''
        extra_kwargs = {
            'url': {'view_name': 'userprofile-detail'},
            'groups': {'view_name': 'basegroup-detail'},
        }
        read_only_fields = ('pk', 'user', 'date_created')

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