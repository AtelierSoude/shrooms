from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework.serializers import HyperlinkedModelSerializer, PrimaryKeyRelatedField, ModelSerializer

"""
FIELDS

"""

User = get_user_model()

"""
SERIALIZERS

"""


class UserShortSerializer(ModelSerializer):
    """
    Short serializer for user
    """
    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'email',
        )
        extra_kwargs = {
            'url': {'view_name': 'user-detail'}
        }


class UserSerializer(HyperlinkedModelSerializer):
    """
    Serializer pour le modèle User
    """
    # user_permissions = PrimaryKeyRelatedField(
    #     queryset=Permission.objects.all(), many=True)

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'email',
            'profile',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
        )
        extra_kwargs = {
            'url': {'view_name': 'user-detail'},
            'profile': {'view_name': 'userprofile-detail'}
        }
        read_only_fields=('id', 'last_login', 'date_joined')


class GroupSerializer(HyperlinkedModelSerializer):
    """
    Serializer pour le modèle Permission de Django
    """
    permissions = PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ('name', 'permissions')
        extra_kwargs = {
            'url': {'view_name': 'group-detail'}
        }
