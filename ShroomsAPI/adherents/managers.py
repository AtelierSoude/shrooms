from datetime import date

from django.db import models

from adherents import models as adh_models


class AdherentManager(models.Manager):
    """
    Manager for proxy model Adherent
    """

    def get_queryset(self):
        "Retrieve all adherents : any UserProfile that has Subscription"
        return super(AdherentManager, self).get_queryset().select_related('user')

    def subscribers(self):
        return self.get_queryset().exclude(
            subscriptions=None)

    def active(self):
        "Retrieve all adherents with a currently active subscription"
        return self.get_queryset().filter(subscriptions__in=adh_models.Subscription.objects.active())

class SubscriptionManager(models.Manager):
    """
    Manager for subscription
    """

    def get_queryset(self):
        "Prefetch subscription type "
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

class SubscriptionTypeManager(models.Manager):
    """
    Manager for subscription types
    """

    def get_queryset(self):
        "Prefetch foreign key status"
        return super(SubscriptionTypeManager, self).get_queryset().select_related('status')
