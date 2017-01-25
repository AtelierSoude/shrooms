from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from adherents.models import Subscription

UserModel = get_user_model()


@receiver(post_save, sender=Subscription)
def adherent_subscribed(sender, instance, created, **kwargs):
    """
    Activity stream : notify subscription
    """
    if created:
        #action.send(instance.adherent, verb=str(_(subscribed)), target = instance )
