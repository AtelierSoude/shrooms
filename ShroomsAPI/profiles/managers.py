from django.db import models


class ShroomManager(models.Manager):
    "Custom manager for Shroom"

    def get_queryset(self):
        "Prefetch shroom's organisation"
        return super(ShroomManager, self).get_queryset().select_related('organisation')

    def get_self(self):
        "Shortcut for retrieving the shroom defining self"
        return self.get_queryset().filter(is_self=True)
