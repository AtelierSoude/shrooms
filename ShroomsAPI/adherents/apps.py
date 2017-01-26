from django.apps import AppConfig


class AdherentsConfig(AppConfig):
    name = 'adherents'
    def ready(self):
        from actstream import registry
        registry.register(
            self.get_model('Adherent'),
            self.get_model('Subscription'))
