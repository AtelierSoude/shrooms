from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        SerializerMethodField)

from adherents.models import Subscription, SubscriptionType


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


class SubscriptionTypeSerializer(HyperlinkedModelSerializer):
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
        )

        extra_kwargs = {
            'url': {'view_name': 'subscriptiontype-detail'}
        }


class SubscriptionSerializer(HyperlinkedModelSerializer):
    """
    SubscriptionType model serializer
    """
    date_end = SerializerMethodField()
    is_active = SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'url',
            'adherent',
            'date_begin',
            'subscription_type',
            'date_end',
            'is_active',
        )

        extra_kwargs = {
            'url': {'view_name': 'subscription-detail'}
        }

    def get_date_end(self, obj):
        return obj.date_end

    def get_is_active(self, obj):
        return obj.is_active
