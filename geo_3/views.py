from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework.generics import ListCreateAPIView

from geo_3.models import Location
from geo_3.serializers import LocationSerializer


class LocationList(ListCreateAPIView):
    """Display locations or add a new one"""
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
