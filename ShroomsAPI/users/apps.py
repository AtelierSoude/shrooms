from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class UsersConfig(AppConfig):
    """
    App config for users module
    """
    name = 'users'
    verbose_name = _('users')
    
'''    def ready(self):
        from actstream import registry
        from django.contrib.auth.models import Permission
        registry.register(self.get_model('User'), Permission)
'''
