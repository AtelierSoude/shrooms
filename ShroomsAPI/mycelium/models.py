from django.db import models
from profiles.models import Organisation

# Create your models here.

class Shroom(models.Model):
    """
     a Shroom identity
    """
    api_url = models.URLField(
        verbose_name='API URL'
    )
    # Shared data : use django's content_type fwk ?
