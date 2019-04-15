from rest_framework import serializers
from geo_3.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for location objects"""

    class Meta:
        model = Location
        fields = ('id', 'name', 'longitude', 'latitude', 'elevation')
