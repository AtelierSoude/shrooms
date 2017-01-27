from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import profiles.models


def validate_is_self(value):
    "Allow only one shroom to define self identity"
    if profiles.models.Shroom.objects.filter(is_self=True).count() == 1:
        if value:
            raise ValidationError(_('You can set only one shroom as self identity'))
