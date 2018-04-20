from rest_framework.test import APIClient, APITestCase
from api.restaurants.views import RestaurantListCreateAPI, RestaurantRUDAPI
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from restaurants.models import Restaurant
from rest_framework import status
from django.conf import settings
import json

User = get_user_model()
client = APIClient()


class RestaurantListCreateAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', password='12345')
        cls.user2 = User.objects.create(username='test2', password='12345')
        cls.restaurant1 = Restaurant.objects.create(name='rest1', owner=cls.user1, category='category1')
        cls.restaurant2 = Restaurant.objects.create(name='rest2', owner=cls.user2, category='category2')

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/api/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(api_reverse('api_restaurants:list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):

        # test get list response
        response = self.client.get(api_reverse('api_restaurants:list-create'), format='json')
        self.assertEqual(len(json.loads(response.content)), Restaurant.objects.filter(owner=self.user1).count())

        # test search list
        self.restaurant3 = Restaurant.objects.create(name='ital', owner=self.user1, category='category3')
        response = self.client.get(api_reverse('api_restaurants:list-create'), data={'qs': 'ita'}, format='json')
        self.assertNotEqual(len(json.loads(response.content)), Restaurant.objects.filter(owner=self.user1).count())

    def test_post(self):

        # test post create restaurant
        response = self.client.post(api_reverse(
            'api_restaurants:list-create'),
            data={
                'name': 'rest4',
                'category': 'category4',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RestaurantRUDAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', password='12345')
        cls.user2 = User.objects.create(username='test2', password='12345')
        cls.restaurant1 = Restaurant.objects.create(name='rest1', owner=cls.user1, category='category1')
        cls.restaurant2 = Restaurant.objects.create(name='rest2', owner=cls.user2, category='category2')

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/api/restaurants/rest1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(self.restaurant1.get_absolute_uri())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):

        # test get restaurant object
        response = self.client.get(self.restaurant1.get_absolute_uri(), format='json')
        self.assertEqual(response.data['name'], self.restaurant1.name)

    def test_post(self):

        # test put, patch, delete

        # put wrong data
        response = self.client.put(self.restaurant1.get_absolute_uri(),
                                   data={'name': 'italiana'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # put good data
        response = self.client.put(self.restaurant1.get_absolute_uri(),
                                   data={
                                       'name': 'italiana',
                                       'category': 'italian'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # patch
        response = self.client.patch(self.restaurant1.get_absolute_uri(),
                                     data={'name': 'pizzaplace'},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # delete
        response = self.client.delete(self.restaurant1.get_absolute_uri())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


