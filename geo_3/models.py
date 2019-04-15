from django.contrib.gis.db import models


class Location(models.Model):
    """Point of interest described by geographical coordinates"""
    name = models.CharField(max_length=128)
    longitude = models.FloatField()
    latitude = models.FloatField()
    elevation = models.IntegerField()
    point = models.PointField(default='POINT(0 0)', srid=4326)

    def __str__(self):
        return self.name
