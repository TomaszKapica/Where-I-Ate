from django.test import TestCase
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant
from django.shortcuts import reverse
from django.conf import settings
from menus.models import Item
from friendship.models import Friend, Follow
User = get_user_model()


class ProfileDetailViewTest(TestCase):
    '''
            Tests ProfileDetailView from profiles.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345', is_active=True)
        cls.user2 = User.objects.create_user(username='test2', password='12345', is_active=True)
        cls.rest1 = Restaurant.objects.create(name='Ital', owner=cls.user2)
        cls.rest2 = Restaurant.objects.create(name='PancakePlace', owner=cls.user2)
        cls.item1 = Item.objects.create(name='pizza', restaurant=cls.rest1, owner=cls.user2)
        cls.item2 = Item.objects.create(name='pancake', restaurant=cls.rest2, owner=cls.user2)

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists_true(self):

        # test if url path exists || existing user

        response = self.client.get('/profile/test1/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_false(self):

        # test if url path exists || not existing user
        response = self.client.get('/profile/test3/')
        self.assertEqual(response.status_code, 404)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse('profiles:detail', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):
        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('profiles:detail', kwargs={'username': self.user1.username}))
        self.assertRedirects(response, '/accounts/login/?next=/profile/test1/')

    def test_correct_template(self):
        # test if template is valid
        response = self.client.get(reverse('profiles:detail', kwargs={'username': self.user1.username}))
        self.assertTemplateUsed(response, 'profiles/profile_detail.html')

    def test_get_without__custom_query(self):
        # test get response
        response = self.client.get(reverse('profiles:detail', kwargs={'username': self.user2.username}))

        # test if response object is same as entry
        self.assertEqual(response.context['object'], self.user2)

        # test restaurants sent to view
        self.assertTrue(response.context['search_query'])
        self.assertQuerysetEqual(
            response.context['search_query'],
            map(repr, Restaurant.objects.filter(owner=self.user2)),
            ordered=False
        )

    def test_get_with_custom_query(self):
        # test get response
        response = self.client.get('/profile/test2/?qs=pizza')

        # test if response object is same as entry
        self.assertEqual(response.context['object'], self.user2)

        # test existing restaurants query
        self.assertTrue(response.context['search_query'])
        self.assertEqual(
            list(response.context['search_query']),
            [self.rest1],
        )

    def test_following(self):

        # tests status of context variable: is_follower
        response1 = self.client.get(reverse('profiles:detail', kwargs={'username': self.user2}))
        self.assertFalse(response1.context['is_follower'])
        Follow.objects.add_follower(
            self.user1,
            self.user2,
        )
        response2 = self.client.get(reverse('profiles:detail', kwargs={'username': self.user2}))
        self.assertTrue(response2.context['is_follower'])

    def test_friendship(self):
        # tests context variables is_requested, is_friend
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])
        response1 = self.client.get(reverse('profiles:detail', kwargs={'username': self.user2}))
        self.assertFalse(response1.context['is_requested'])
        self.assertFalse(response1.context['is_friend'])
        friend = Friend.objects.add_friend(
            self.user1,
            self.user2,
            message='I would like to be your friend.'
        )

        response2 = self.client.get(reverse('profiles:detail', kwargs={'username': self.user2}))
        self.assertTrue(response2.context['is_requested'])
        self.assertFalse(response2.context['is_friend'])

        friend.accept()
        response3 = self.client.get(reverse('profiles:detail', kwargs={'username': self.user2}))
        self.assertTrue(response3.context['is_friend'])




