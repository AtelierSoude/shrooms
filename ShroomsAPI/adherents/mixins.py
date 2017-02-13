from adherents.models import Adherent
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from datetime import date
from users.serializers import UserShortSerializer

class SubscriptionSerializerMixin(object):
    """
    Mixin for Subscriptions serializers adding common methods
    """
    is_active = serializers.SerializerMethodField()

    def get_is_active(self, obj):
        return obj.is_active

    def validate(self, data):
        try:
            adh = Adherent.objects.get(pk=data['adherent'].pk)
            date_begin = getattr(data, 'date_begin', date.today())
            date_end = getattr(data, 'date_end', None) or date_begin + data['subscription_type'].duration
            error_str = _("This date overlaps with existing subscription for this adherent. "
                          "You may explicitly set the subscription's date interval to avoid overlapping subscriptions.")

            for subscription in adh.subscriptions.all():
                if subscription.overlaps(date_begin):
                    raise serializers.ValidationError(
                        {'date_begin': error_str})
                if subscription.overlaps(date_begin):
                    raise serializers.ValidationError(
                        {'date_begin': error_str})
                return data
        except Adherent.DoesNotExist:
            return data

class AdherentSerializerMixin(object):
    """
    Mixin for serializing Adherent
    Provides status field and serialized user informations
    """
    user = UserShortSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        "Getter for status field"
        return obj.status
