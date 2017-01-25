from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

"""
Models RegistrationProfile,...
are imported from the django registration project
"""


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', ]
    email = models.EmailField(_('email address'), blank=False, null=False)
    pass
