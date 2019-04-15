from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework.generics import ListCreateAPIView

from geo_3.models import Location
from geo_3.serializers import LocationSerializer


class LocationList(ListCreateAPIView):
    """Display locations or add a new one"""
    serializer_class = LocationSerializer

    def get_queryset(self):
        """Find closest location or search given perimeter"""
        longitude = self.request.query_params.get('user_longitude')
        latitude = self.request.query_params.get('user_latitude')
        perimeter = self.request.query_params.get('perimeter')
        print('longitude: ', longitude)
        print('latitude: ', latitude)
        print('perimeter: ', perimeter)
        queryset = self.queryset
        if longitude and latitude and perimeter:
            try:
                user_pnt = fromstr(
                    'POINT({} {})'.format(
                        longitude, latitude), srid=4326
                )
                queryset = Location.objects.filter(
                    point__distance_lte=(user_pnt, D(km=abs(int(perimeter)))))
            except (ValueError, TypeError):
                print('Error, please enter numbers')
            print('queryset: ', queryset)
        elif longitude and latitude:
            try:
                user_pnt = fromstr(
                    'POINT({} {})'.format(
                        longitude, latitude), srid=4326
                )
                queryset = Location.objects.annotate(
                    distance=Distance(
                        user_pnt, 'point')).order_by('distance')[:1]
            except (ValueError, TypeError):
                print('Error, please enter numbers')
            print('queryset: ', queryset)
        return queryset

    def perform_create(self, serializer):
        """Create a new Location object"""
        longitude = serializer.validated_data['longitude']
        latitude = serializer.validated_data['latitude']
        serializer.validated_data['point'] = fromstr(
            'POINT({} {})'.format(
                longitude, latitude), srid=4326
        )
        print('serializer_data: ', serializer.validated_data)
        if serializer.is_valid:
            serializer.save()
