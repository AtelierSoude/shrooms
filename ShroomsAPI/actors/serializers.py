from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from .models import (
    Individual,
    Adherent,
    Subscription,
    SubscriptionType,
    Organisation
)
import datetime

"""
FIELDS

"""


"""
SERIALIZERS

"""


class IndividualSerializer(HyperlinkedModelSerializer):
    """
    Serializer pour le modèle User
    """
    adherent = HyperlinkedRelatedField(
        view_name='adherent-detail',
        read_only=True
    )
    class Meta:
        model = Individual
        fields = (
            'url',
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'user',
            'groups',
            'phone_number',
            'newsletter_subscription',
            'email',
            'date_created',
            'about',
            'website',
            'adherent',
        )
        extra_kwargs = {
            'url': {'view_name': 'individual-detail'}
        }


class AdherentSerializer(HyperlinkedModelSerializer):
    """
    Adherent model serializer
    """
    individual = HyperlinkedIdentityField(view_name='individual-detail')

    class Meta:
        model = Adherent
        fields = (
            'url',
            'subscription_date',
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'user',
            'groups',
            'phone_number',
            'newsletter_subscription',
            'email',
            'date_created',
            'about',
            'website',
            'subscription_set',
            'individual'
        )
        extra_kwargs = {
            'url': {'view_name': 'adherent-detail'}
        }

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
        model=Subscription
        fields= (
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
        return obj.date_begin + obj.subscription_type.duration
    def get_is_active(self, obj):
        today = datetime.date.today()
        return today > obj.date_begin and today < self.get_date_end(obj)

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
            'contact',
            'groups',
            'phone_number',
            'newsletter_subscription',
            'email',
            'date_created',
            'about',
            'website',
        )
        extra_kwargs = {
            'url': {'view_name': 'organisation-detail'}
        }