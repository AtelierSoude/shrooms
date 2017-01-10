from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    App config for users module
    """
    name = 'users'

    def ready(self):
        from actstream import registry
        from django.contrib.auth.models import Permission
        registry.register(self.get_model('User'), Permission)
