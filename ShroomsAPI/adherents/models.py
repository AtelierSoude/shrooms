from datetime import date, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils import timezone

from profiles.models import UserProfile
# from model_utils import Choices
# from model_utils.fields import StatusField


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


class AdherentManager(models.Manager):
    """
    Manager for proxy model Adherent
    """

    def get_queryset(self):
        "Retrieve all adherents : any UserProfile that has Subscription"
        return super(AdherentManager, self).get_queryset().exclude(
            subscriptions=None)

    def active(self):
        "Retrieve all adherents with a currently active subscription"
        return self.get_queryset().filter(subscriptions__in=Subscription.objects.active())


class Adherent(UserProfile):
    """
    UserProfile proxy model for adherents
    """
    objects = AdherentManager()

    @cached_property
    def active_subscription(self):
        "Returns  currently active subscription for the adherent"
        today = date.today()
        return self.subscriptions.filter(date_end__gte=today, date_begin__lte=today)

    @cached_property
    def status(self):
        "Adherent instance's status based on currently active subscription"
        return self.active_subscription.subscription_type.status

    class Meta:
        proxy = True
        verbose_name = _('adherent')


class SubscriptionTypeManager(models.Manager):
    """
    Manager for subscription types
    """

    def get_queryset(self):
        "Prefetch foreign key status"
        return super(SubscriptionTypeManager, self).get_queryset().select_related('status')


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

    objects = SubscriptionTypeManager()

    def __str__(self):
        return '%s [%s]' % (self.name, self.status)

    class Meta:
        verbose_name = _("subscription type")
        verbose_name_plural = _("subscription types")


class SubscriptionManager(models.Manager):
    """
    Manager for subscription
    """

    def get_queryset(self):
        "Prefetch subscription type along with subscription"
        return super(SubscriptionManager, self).get_queryset().select_related('subscription_type__status')

    def active(self):
        "Get currently active subscriptions"
        today = date.today()
        return self.get_queryset().filter(date_begin__lte=today).annotate(
            expiration_date=models.ExpressionWrapper(
                models.F('date_begin') +
                models.F('subscription_type__duration'),
                output_field=models.DateField()
            )
        ).filter(expiration_date__gte=today)


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

    @cached_property
    def is_active(self):
        "Get the current state for the subscription"
        today = date.today()
        if self.date_begin <= today and self.date_end >= today:
            return True
        else:
            return False

    def __str__(self):
        return "%s %s [%s]" % (
            self.adherent,
            self.date_begin, _("Active") if self.is_active else _("Expired"))

    objects = SubscriptionManager()

    class Meta:
        verbose_name = _("subscription")
