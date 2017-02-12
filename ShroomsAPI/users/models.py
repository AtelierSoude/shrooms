from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from dry_rest_permissions.generics import allow_staff_or_superuser, authenticated_users
"""
Models RegistrationProfile,...
are imported from the django registration project
"""


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', ]
    email = models.EmailField(_('email address'), blank=False, null=False)

    # DRY permissions
    

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return False
    
    @staticmethod
    @authenticated_users
    def has_retrieve_permission(request):
        return True
    
    def has_object_read_permission(self, request):
        return request.user == self
    
    def has_object_update_permission(self, request):
        return request.user == self
    
    @allow_staff_or_superuser
    def has_object_destroy_permission(self, request):
        return False


