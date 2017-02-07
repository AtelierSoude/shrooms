from datetime import date

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from adherents.models import Subscription, SubscriptionType
from adherents.mixins import SubscriptionSerializerMixin

"""
FIELDS

"""


"""
SERIALIZERS

"""

class SubscriptionTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    SubscriptionType model SubscriptionTypeSerializer
    """
    class Meta:
        model = SubscriptionType
        fields = (
            'url',
            'price',
            'duration',
            'name',
            'subscription_set'
        )

        extra_kwargs = {
            'url': {'view_name': 'subscriptiontype-detail'},
            'subscription_set' : {'view_name' : 'subscription-detail'}
        }


class SubscriptionSerializer(SubscriptionSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    SubscriptionType model serializer
    """

    class Meta:
        model = Subscription
        fields = (
            'url',
            'adherent',
            'date_begin',
            'date_end',
            'subscription_type',
            'is_active',
        )

        extra_kwargs = {
            'url': {'view_name': 'subscription-detail'},
            'adherent': {'view_name': 'userprofile-detail'},
            'subscription_type': {'view_name': 'subscriptiontype-detail'},
        }



class CurrentProfileDefault(object):
    "Allows setting current user profile as default in subscription serializer"
    profile = None

    def set_context(self, serializer_field):
        "Get current user profile"
        self.profile = getattr(serializer_field.context['request'].user, 'profile', None)

    def __call__(self):
        return self.profile

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class SubscribeSerializer(SubscriptionSerializerMixin, serializers.ModelSerializer):
    "Subscribe serializer, sets current user as subscribing user"

    adherent = serializers.HiddenField(
        default=CurrentProfileDefault()
    )

    def validate_adherent(self, value):
        "Check that adherent's user profile provide sufficient informations"
        if value.has_name_info is False:
            raise serializers.ValidationError(
                _("Incomplete user profile : please provide first and last name "
                  "to be allowed to subscribe.")
            )
        return value
    class Meta:
        model = Subscription
        fields = (
            'adherent',
            'date_begin',
            'date_end',
            'subscription_type'
        )
        
