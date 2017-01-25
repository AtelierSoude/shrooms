from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a new profile for the newly registered user
    """
    if created:
        #action.send(instance, verb=str(_(registered)))
        pass
