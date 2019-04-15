from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from geo_3.models import Location
from geo_3.serializers import LocationSerializer

LOCATION_URL = reverse('locations')


class LocationTestCase(TestCase):
    """Test Location requests"""

    def setUp(self):
        self.client = APIClient()

    def test_creating_location(self):
        """Creating new location"""
        data = {
            'name': 'test_location',
            'longitude': 51.123456,
            'latitude': 21.123456,
            'elevation': 138
        }
        res = self.client.post(LOCATION_URL, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        location = Location.objects.get(id=res.data['id'])
        for key in data.keys():
            self.assertEqual(data[key], getattr(location, key))

    def test_retrieving_location(self):
        """Test retrieving a list of locations"""

        locations = Location.objects.all().order_by('-id')
        serializer = LocationSerializer(locations, many=True)

        res = self.client.get(LOCATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieving_locations_based_on_user_data(self):
        """Test getting user location params"""
        data = {
            'user_name': 'Test_user',
            'user_longitude': 51.123456,
            'user_latitude': 21.123456,
            'perimeter': 300
        }

        locations = Location.objects.filter(
            point__distance_lte=(
                Point(data['user_longitude'],
                      data['user_latitude'],
                      srid=4326),
                D(km=abs(int(data['perimeter'])))))

        serializer = LocationSerializer(locations, many=True)

        res = self.client.get(LOCATION_URL, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_if_error_when_incorrect_data_in_user_form(self):
        """Test raising Value Error"""
        with self.assertRaises(TypeError):
            data = {
                'user_name': 'Test_user',
                'user_longitude': '51.123456',
                'user_latitude': '21.123456',
                'perimeter': 'jdjdj'
            }

            Location.objects.filter(point__distance_lte=(
                Point(data['user_longitude'],
                      data['user_latitude'],
                      srid=4326),
                D(km=abs(int(data['perimeter'])))))

            self.client.get(LOCATION_URL, data, format='json')
