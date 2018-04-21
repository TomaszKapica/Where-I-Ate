from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from menus.models import Item
from restaurants.models import Restaurant
from rest_framework import status
from django.conf import settings
import json

User = get_user_model()
client = APIClient()


class ItemListCreateAPITest(APITestCase):

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
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(api_reverse('api_items:list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):

        # test get list response
        response = self.client.get(api_reverse('api_items:list-create'), format='json')
        self.assertEqual(len(json.loads(response.content)), Item.objects.filter(owner=self.user1).count())

        # test search list
        self.item3 = Item.objects.create(name='randitem', owner=self.user1, restaurant=self.restaurant1)
        response = self.client.get(api_reverse('api_items:list-create'), data={'qs': 'rand'}, format='json')
        self.assertNotEqual(len(json.loads(response.content)), Item.objects.filter(owner=self.user1).count())

    def test_validate(self):

        # test post create item
        response = self.client.post(api_reverse(
            'api_items:list-create'),
            data={
                'name': 'item4',
                'owner': self.user1,
                'restaurant': 1,
                'contents': 'some random content'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ItemRUDAPITest(APITestCase):

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
        response = self.client.get('/api/items/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(self.item1.get_absolute_uri())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):

        # test get item object
        response = self.client.get(self.item1.get_absolute_uri(), format='json')
        self.assertEqual(response.data['name'], self.item1.name)

    def test_post(self):

        # test put, patch, delete

        # put
        response = self.client.put(self.item1.get_absolute_uri(),
                                   data={
                                       'name': 'randitem',
                                       'owner': self.user1,
                                       'restaurant': 1,
                                       'contents': 'some random content'
                                   },
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # patch
        response = self.client.patch(self.item1.get_absolute_uri(),
                                     data={
                                         'name': 'carbonara',
                                         'restaurant': 1
                                     }
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # delete
        response = self.client.delete(self.item1.get_absolute_uri())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)