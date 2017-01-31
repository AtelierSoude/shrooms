from datetime import date, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils import timezone

from profiles.models import UserProfile
from adherents import managers



class AdherentStatus(models.Model):
    """
    Group extension for managing adherent statuses
    """
    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
        null=False,
        blank=False,
    )

    def __str__(self):
        return "%s" % (self.name,)

    class Meta:
        verbose_name = _('adherent\'s status')
        verbose_name_plural = _('adherents\' statuses')


class Adherent(UserProfile):
    """
    UserProfile proxy model for adherents
    """
    objects = managers.AdherentManager()

    @cached_property
    def active_subscription(self):
        "Returns  currently active subscription for the adherent"
        today = date.today()
        return self.subscriptions.filter(date_end__gte=today, date_begin__lte=today).get()

    @cached_property
    def status(self):
        "Adherent instance's status based on currently active subscription"
        return self.active_subscription.subscription_type.status

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
    status = models.ForeignKey(
        'AdherentStatus',
        blank=False,
        null=False,
    )

    objects = managers.SubscriptionTypeManager()

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
        related_name='subscriptions'
    )
    date_begin = models.DateField(
        null=False,
        blank=True,
        default=timezone.now,
        verbose_name=_('start date'),
    )
    date_end = models.DateField(
        null=False,
        blank=True,
        verbose_name=_('expiration date')
    )
    time_created = models.DateTimeField(
        null=False,
        auto_now_add=True,
        verbose_name=_('time created')
    )
    subscription_type = models.ForeignKey(
        'SubscriptionType',
        null=False,
        blank=False,
        verbose_name=_('subscription type'),
    )

    def save(self, *args, **kwargs):
        if self.date_end is None:
            self.date_end = self.date_begin + self.subscription_type.duration
        super(Subscription, self).save(*args, **kwargs)

    def overlaps(self, overlapping_date):
        "Checks if a date interval overlaps with subscription date interval"
        if overlapping_date <= self.date_end and overlapping_date >= self.date_begin:
            return True
        else:
            return False

    @cached_property
    def is_active(self):
        "Get the current state for the subscription"
        today = date.today()
        if self.date_begin <= today and self.date_end >= today:
            return True
        else:
            return False

    def __str__(self):
        return "%s : %s" % (
            self.adherent,
            self.subscription_type)

    objects = managers.SubscriptionManager()

    class Meta:
        verbose_name = _("subscription")
