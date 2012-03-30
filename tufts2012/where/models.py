from django.db import models

class Location(models.Model):
    """ The location of a student
    """
    lat = models.DecimalField(max_digits=6, decimal_places=3)
    lon = models.DecimalField(max_digits=6, decimal_places=3)
    name = models.CharField(max_length=50) # The english name for the location
