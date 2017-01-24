from django.contrib.auth import get_user_model
from rest_framework.serializers import HyperlinkedModelSerializer, PrimaryKeyRelatedField, ModelSerializer

"""
FIELDS

"""


"""
SERIALIZERS

"""


class UserRegistrationSerializer(ModelSerializer):
    """
    User serializer for registering new accounts
    """
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password',
        )

class UserActivatedSerializer(ModelSerializer):
    """
    User serializer sent by successful activation response
    """
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'is_active',
        )
