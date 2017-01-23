from datetime import date, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from profiles.models import UserProfile
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
        verbose_name = _('adherent')


class SubscriptionType(models.Model):
    """
    Contains all available subscriptions,
    defines duration (default=1 year), price and status
    """
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('price'),
    )
    duration = models.DurationField(
        default=timedelta(days=365),
        verbose_name=_('duration'),
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=_('name')
    )
    STATUS = Choices('Actif', 'Participant')
    status = StatusField(
        verbose_name=_('status'),
    )

    def __str__(self):
        return '%s [%s]' % (self.name, self.status)

    class Meta:
        verbose_name = _("subscription type")
        verbose_name_plural = _("subscription types")

class Subscription(models.Model):
    """
    Handles subscriptions for Adherents, including
    status, price and validity date range.
    """
    adherent = models.ForeignKey(
        'profiles.UserProfile',
        null=False,
        blank=False,
        verbose_name=_('adherent'),
    )
    date_begin = models.DateField(
        null=False,
        auto_now_add=True,
        verbose_name=_('start date'),
    )
    subscription_type = models.ForeignKey(
        'SubscriptionType',
        null=False,
        blank=False,
        verbose_name=_('subscription type'),
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
        return "%s %s [%s]" % (self.adherent, self.date_begin, _("Active") if self.is_active else _("Expired"))

    class Meta:
        verbose_name = _("subscription")
