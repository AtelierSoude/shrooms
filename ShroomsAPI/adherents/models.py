from datetime import timedelta, date

from django.db import models

from actors.models import UserProfile
from model_utils import Choices
from model_utils.fields import StatusField


# Create your models here.

class AdherentManager(models.Manager):
    """
    Manager for proxy model Adherent
    """

    def get_queryset(self):
        "Retrieve all adherents : any UserProfile that has Subscription"
        return super(AdherentManager, self).get_queryset().exclude(subscription=None)

    def active(self):
        "Retrieve all adherents with a currently active subscription"
        return self.get_queryset().filter(subscription__is_active=True)


class Adherent(UserProfile):
    """
    UserProfile proxy model for adherents
    """
    objects = AdherentManager()

    class Meta:
        proxy = True


class SubscriptionType(models.Model):
    """
    Contains all available subscriptions,
    defines duration (default=1 year), price and status
    """
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    duration = models.DurationField(
        default=timedelta(days=365)
    )
    name = models.CharField(
        max_length=50,
        blank=False
    )
    STATUS = Choices('Actif', 'Participant')
    status = StatusField()

    def __str__(self):
        return '%s [%s]' % (self.name, self.status)


class Subscription(models.Model):
    """
    Handles subscriptions for Adherents, including
    status, price and validity date range.
    """
    adherent = models.ForeignKey(
        'actors.UserProfile',
        null=False,
        blank=False
    )
    date_begin = models.DateField(
        null=False,
        auto_now_add=True
    )
    subscription_type = models.ForeignKey(
        'SubscriptionType',
        null=False,
        blank=False
    )

    @property
    def date_end(self):
        """
        Returns the calculated expiration date for the subscription
        from the subscription type
        """
        return self.date_begin + self.subscription_type.duration

    @property
    def is_active(self):
        "Returns the current state for the subscription"
        today = date.today()
        if self.date_begin <= today and self.date_end >= today:
            return True
        else:
            return False
    
    def __str__(self):
        return "%s %s [%s]" % (self.adherent, self.date_begin, "Active" if self.is_active else "Expired")
