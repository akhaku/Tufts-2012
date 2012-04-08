from django.contrib.auth.models import User
from django.db import models

class Location(models.Model):
    """ The location of a student
    """
    lat = models.DecimalField(max_digits=6, decimal_places=3)
    lon = models.DecimalField(max_digits=6, decimal_places=3)
     # The english name for the location
    name = models.CharField(max_length=50, help_text="Location")
    user = models.ForeignKey(User, related_name="location")

    def __unicode__(self):
        return self.name
