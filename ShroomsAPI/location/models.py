from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField
# Create your models here.

class Place(models.Model):
    country = models.CharField()
    state = models.CharField(max_length=50, blank=True, null=True)
    
    locality = models.CharField()
    location = GeopositionField()