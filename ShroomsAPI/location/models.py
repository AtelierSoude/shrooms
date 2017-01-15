from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField
# Create your models here.

class Place(models.Model):
    city = models.CharField()
    location = LocationField(based_fields=['city'],
                             initial=Point(-49.1607606, -22.2876834))