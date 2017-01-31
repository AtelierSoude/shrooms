from datetime import date

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from adherents.models import Adherent, Subscription, SubscriptionType


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
        )

        extra_kwargs = {
            'url': {'view_name': 'subscriptiontype-detail'}
        }


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    SubscriptionType model serializer
    """
    is_active = serializers.SerializerMethodField()

    def validate(self, data):
        try:
            adh = Adherent.objects.get(pk=data['adherent'].pk)
            date_end = getattr(data, 'date_end', None) or data[
                'date_begin'] + data['subscription_type'].duration
            error_str = _("This date overlaps with existing subscription for this adherent. "
                          "You may explicitly set the subscription's date interval to avoid overlapping subscriptions.")

            for subscription in adh.subscriptions.all():
                if subscription.overlaps(data['date_begin']):
                    raise serializers.ValidationError(
                        {'date_begin': error_str})
                if subscription.overlaps(data['date_begin']):
                    raise serializers.ValidationError(
                        {'date_begin': error_str})
                return data
        except Adherent.DoesNotExist:
            return data

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
            'url',
            'adherent',
            'date_begin',
            'date_end',
            'subscription_type',
            'is_active',
        )

        extra_kwargs = {
            'url': {'view_name': 'subscription-detail'}
        }

    def get_is_active(self, obj):
        return obj.is_active
