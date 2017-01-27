from profiles.models import Shroom
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

def validate_is_self(value):
    "Allow only one shroom to define self identity"
    if Shroom.objects.filter(is_self=True).count() == 1:
        if value:
            raise ValidationError(_('You can set only one shroom as self identity'))

