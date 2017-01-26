from actstream import action
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def activity_user_registered(sender, instance, created, **kwargs):
    """
    Activity stream : notify new user registered
    """
    if created:
        action.send(instance, verb=str(_('registered')))
