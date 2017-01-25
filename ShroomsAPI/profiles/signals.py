from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Organisation, OrganisationGroup, UserProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a new profile for the newly registered user
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Organisation)
def create_organisation_group(sender, instance, created, **kwargs):
    """
    Create a new organisation group for the new Organisation
    """
    if created:
        OrganisationGroup.objects.create(organisation=instance)
