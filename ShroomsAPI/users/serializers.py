from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)


"""
FIELDS

"""


"""
SERIALIZERS

"""


class AllFieldsHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    """
    Serializer qui inclut tous les champs d'un modèle
    et permet d'y ajouter des champs supplémentaires
    (comme url pour une API navigable avec DRF par ex)
    """

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(AllFieldsHyperlinkedModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
    class Meta :
        pass


class UserSerializer(AllFieldsHyperlinkedModelSerializer):
    """
    Serializer pour le modèle User
    """
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_field = ['url']
        extra_kwargs = {
            'url': {'view_name': 'user-detail'}
        }

class PermissionSerializer(AllFieldsHyperlinkedModelSerializer):
    """
    Serializer pour le modèle Permission de Django
    """
    class Meta:
        model = Permission
        fields = '__all__'
        extra_field = ['url']
        extra_kwargs = {
            'url': {'view_name': 'permission-detail'}
        }
