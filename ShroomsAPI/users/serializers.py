from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import permissions
from rest_framework.serializers import HyperlinkedModelSerializer

"""
FIELDS

"""


"""
SERIALIZERS

"""


class UserSerializer(HyperlinkedModelSerializer):
    """
    Serializer pour le modèle User
    """
    class Meta:
        model = get_user_model()
        fields = (
            'url',
            'last_login',
            'is_superuser',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'groups',
            'user_permissions',
        )
        extra_kwargs = {
            'url': {'view_name': 'user-detail'}
        }


class PermissionSerializer(HyperlinkedModelSerializer):
    """
    Serializer pour le modèle Permission de Django
    """
    class Meta:
        model = Permission
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'permission-detail'}
        }

