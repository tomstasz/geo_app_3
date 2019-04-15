from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework.generics import ListCreateAPIView

from geo_3.models import Location
from geo_3.serializers import LocationSerializer


class LocationList(ListCreateAPIView):
    """Display locations or add a new one"""
    serializer_class = LocationSerializer

    def perform_create(self, serializer):
        """Create a new Location object"""
        longitude = serializer.validated_data['longitude']
        latitude = serializer.validated_data['latitude']
        serializer.validated_data['point'] = fromstr(
            'POINT({} {})'.format(
                longitude, latitude), srid=4326
        )
        print('ser_data: ', serializer.validated_data)
        if serializer.is_valid:
            serializer.save()
