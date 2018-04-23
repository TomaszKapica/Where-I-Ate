from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from users.models import RestaurantUser
from restaurants.models import Restaurant
from menus.models import Item
from rest_framework import status
from django.conf import settings
import json

User = get_user_model()
client = APIClient()


class ProfilesListAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', password='12345')
        cls.user2 = User.objects.create(username='test2', password='12345')
        cls.restaurant1 = Restaurant.objects.create(name='rest1', owner=cls.user1, category='category1')
        cls.restaurant2 = Restaurant.objects.create(name='rest2', owner=cls.user2, category='category2')
        cls.item1 = Item.objects.create(name='item1', owner=cls.user1, restaurant=cls.restaurant1)
        cls.item2 = Item.objects.create(name='item2', owner=cls.user2, restaurant=cls.restaurant2)

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(api_reverse('api_profiles:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):

        # test get list response
        response = self.client.get(api_reverse('api_profiles:list'), format='json')
        self.assertEqual(len(json.loads(response.content)), RestaurantUser.objects.all().count())

        # test search
        self.user1 = User.objects.create(username='randuser', password='12345')
        response = self.client.get(api_reverse('api_profiles:list'),
                                   data={
                                       'qs': 'rand',
                                       'username': 'randstr'
                                   },
                                   format='json')
        filtered = RestaurantUser.objects.filter(username__icontains='rand').count()
        self.assertEqual(len(json.loads(response.content)), filtered)


class ProfilesRetrieveAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', password='12345')
        cls.user2 = User.objects.create(username='test2', password='12345')
        cls.restaurant1 = Restaurant.objects.create(name='rest1', owner=cls.user1, category='category1')
        cls.restaurant2 = Restaurant.objects.create(name='rest2', owner=cls.user2, category='category2')
        cls.item1 = Item.objects.create(name='item1', owner=cls.user1, restaurant=cls.restaurant1)
        cls.item2 = Item.objects.create(name='item2', owner=cls.user2, restaurant=cls.restaurant2)

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/api/profiles/test1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(self.user1.get_absolute_uri())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):

        # test get item object
        response = self.client.get(self.user1.get_absolute_uri(), format='json')
        restaurants = Restaurant.objects.filter(owner=self.user1)[0]

        self.assertEqual(response.data['restaurant_set'][0]['name'], restaurants.name)
