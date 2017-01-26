from django.db import models
from profiles.models import Organisation

# Create your models here.

class Shroom(models.Model):
    """
    A Shroom identity
    """
    api_url = models.URLField(
        verbose_name='API URL'
    )
    organisation = models.OneToOneField(
        Organisation,
        blank=False,
        null=False,
    )
    # Shared data : use django's content_type fwk ?
