from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework.serializers import HyperlinkedModelSerializer, PrimaryKeyRelatedField

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
    user_permissions = PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True)

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
