from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from dry_rest_permissions.generics import allow_staff_or_superuser, authenticated_users
"""
Models RegistrationProfile,...
are imported from the django registration project
"""


class User(AbstractUser):
    """
    Subclass of Django User model
    """
    REQUIRED_FIELDS = ['email', ]
    email = models.EmailField(_('email address'), blank=False, null=False)

    def __str__(self):
        return "@%s" % self.username

    """
    DRY permissions :
    Users API endpoint may be read by any auth User
    Write operations are reserved to admins.
    """

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        "Lock all writing access except for admin"
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        "Lock object writing except for admin"
        return False

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        "Allow read access for auth users"
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        "Allow object read access for auth users"
        return True
