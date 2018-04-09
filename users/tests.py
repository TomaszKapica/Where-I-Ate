from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import settings
from django.urls import reverse
from friendship.models import Follow, Friend, FriendshipRequest
from restaurants.models import Restaurant
from menus.models import Item

User = get_user_model()


class FriendListViewTest(TestCase):
    '''
    Tests FriendListView from users.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.user2 = User.objects.create_user(username='test2', password='12345')
        Friend.objects.add_friend(
            cls.user2,
            cls.user1,
            message='I would like to be your friend.'
        )
        friend = FriendshipRequest.objects.all()[0]
        friend.accept()

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/user/friends/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse("users:friend-list"))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('users:friend-list'))
        self.assertRedirects(response, '/accounts/login/?next=/user/friends/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse("users:friend-list"))
        self.assertTemplateUsed(response, 'users/friends-list.html')

    def test_get(self):

        # test get response
        response = self.client.get(reverse("users:friend-list"))
        obj = response.context['object_list']
        self.assertQuerysetEqual(obj, map(repr, Friend.objects.friends(self.user1)), ordered=False)
        self.assertEqual(list(response.context['object_list']), [self.user2])
        self.assertEqual(response.context['title'], 'My Friends')

    def test_post(self):

        # test post response

        # friendship status before
        self.assertTrue(Friend.objects.friends(self.user1))

        response1 = self.client.post(reverse("users:friend-list"),
                         data={
                             'path': reverse('users:friend-list'),
                             'status': 'not_del',
                             'username': self.user2.username,
                         }
                         )

        #friendship status after| wrong atribute:status
        self.assertTrue(Friend.objects.friends(self.user1))

        response2 = self.client.post(reverse("users:friend-list"),
                         data={
                             'path': reverse('users:friend-list'),
                             'status': 'deleted',
                             'username': self.user2.username,
                         }
                                     )

        # frienship status after delete
        self.assertFalse(Friend.objects.friends(self.user1))


class FriendToggleViewTest(TestCase):
    '''
    Tests FriendshipToggleView from users.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.user2 = User.objects.create_user(username='test2', password='12345')

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.post('/user/friend-add/',
                                    data={'path': reverse('profiles:detail', kwargs={'username': self.user2.username})})
        self.assertEqual(response.status_code, 302)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.post(reverse("users:friend-add"),
                                    data={'path': reverse('profiles:detail', kwargs={'username': self.user2.username})})
        self.assertEqual(response.status_code, 302)

    def test_not_logged(self):
        # test login requirement
        self.client.logout()
        response = self.client.post(reverse("users:friend-add"),
                                    data={'path': reverse('profiles:detail', kwargs={'username': self.user2.username})})
        self.assertRedirects(response, '/accounts/login/?next=/user/friend-add/')

    def test_post(self):
        # test post response

        # friendship status before
        self.assertFalse(Friend.objects.friends(self.user1))

        self.client.post(reverse("users:friend-add"),
                                     data={
                                         'path': reverse('profiles:detail', kwargs={'username': self.user2.username}),
                                         'status': 'default_status',
                                         'username': self.user2.username,
                                     }
                                     )

        # friendship status after| wrong atribute 'status'
        self.assertFalse(Friend.objects.friends(self.user1))

        self.client.post(reverse("users:friend-add"),
                                     data={
                                         'path': reverse('profiles:detail', kwargs={'username': self.user2.username}),
                                         'status': 'not_friend',
                                         'username': self.user2.username,
                                     }
                                     )

        # frienship status with attribute 'status': 'not_friend'

        self.assertTrue(Friend.objects.sent_requests(self.user1))
        friend = Friend.objects.sent_requests(self.user1)[0]
        friend.accept()
        self.assertTrue(Friend.objects.friends(self.user1))
        self.assertEqual(Friend.objects.friends(self.user1), [self.user2])

        self.client.post(reverse("users:friend-add"),
                                     data={
                                         'path': reverse('profiles:detail', kwargs={'username': self.user2.username}),
                                         'status': 'is_friend',
                                         'username': self.user2.username,
                                    }
                        )

        # frienship status with attribute 'status': 'is_friend'
        self.assertFalse(Friend.objects.friends(self.user1))


class FriendshipRequestViewTest(TestCase):
    '''
    Tests FriendshipToggleView from users.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.user2 = User.objects.create_user(username='test2', password='12345')
        cls.user3 = User.objects.create_user(username='test3', password='12345')
        cls.user4 = User.objects.create_user(username='test4', password='12345')

        for i in range(3):
            Friend.objects.add_friend(
                User.objects.filter(username='test{}'.format(i+2))[0],
                cls.user1,
                message='I would like to be your friend.'
            )

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/user/requests/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse("users:requests"))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):
        # test login requirement
        self.client.logout()
        response = self.client.get(reverse("users:requests"))
        self.assertRedirects(response, '/accounts/login/?next=/user/requests/')

    def test_get(self):

        # test get response
        response = self.client.get(reverse("users:requests"))
        obj = response.context['object_list']
        self.assertQuerysetEqual(obj, map(repr, Friend.objects.unrejected_requests(self.user1)), ordered=False)
        self.assertEqual(response.context['title'], 'Friendship Requests')
        self.assertEqual(response.context['title_1'], 'Requested by')
        self.assertEqual(response.context['title_2'], 'My Requests')

    def test_post(self):
        # test post response

        # friend requests status
        self.assertEqual(Friend.objects.unrejected_request_count(self.user1), 3)
        self.assertFalse(Friend.objects.rejected_requests(self.user1))

        self.client.post(reverse("users:requests"),
                                     data={
                                         'path': reverse('users:requests'),
                                         'status': 'accepted',
                                         'req_id': FriendshipRequest.objects.filter(from_user=self.user2)[0].id,
                                     }
                                     )

        # test if user was added to friends
        self.assertTrue(Friend.objects.friends(self.user1))

        self.client.post(reverse("users:requests"),
                         data={
                             'path': reverse('users:requests'),
                             'status': 'rejected',
                             'req_id': FriendshipRequest.objects.filter(from_user=self.user3)[0].id,
                         }
                         )

        # test if request was cancelled
        self.assertTrue(Friend.objects.rejected_requests(self.user1))

        self.client.post(reverse("users:requests"),
                         data={
                             'path': reverse('users:requests'),
                             'status': 'cancelled',
                             'req_id': FriendshipRequest.objects.filter(from_user=self.user4)[0].id,
                         }
                         )

        # test if user was rejected | 1 is from rejected
        self.assertEqual(len(Friend.objects.requests(self.user1)), 1)


class FollowListViewTest(TestCase):
    '''
    Tests FollowListView from users.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.user2 = User.objects.create_user(username='test2', password='12345')
        cls.user3 = User.objects.create_user(username='test3', password='12345')
        Follow.objects.add_follower(
            cls.user1,
            cls.user2,
        )
        Follow.objects.add_follower(
            cls.user3,
            cls.user1,
        )

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/user/follow/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse("users:follow-list"))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('users:follow-list'))
        self.assertRedirects(response, '/accounts/login/?next=/user/follow/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse("users:follow-list"))
        self.assertTemplateUsed(response, 'users/follow-list.html')

    def test_get(self):

        # test get response
        response = self.client.get(reverse("users:follow-list"))
        obj1 = response.context['object_list']
        obj2 = response.context['followed_by']
        self.assertQuerysetEqual(obj1, map(repr, Follow.objects.following(self.user1)), ordered=False)
        self.assertQuerysetEqual(obj2, map(repr, Follow.objects.followers(self.user1)), ordered=False)
        self.assertEqual(response.context['title'], 'Follow')
        self.assertEqual(response.context['title_1'], 'My Followings')
        self.assertEqual(response.context['title_2'], 'People following me')


class FollowToggleViewTest(TestCase):
    '''
    Tests FollowToggleView from users.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.user2 = User.objects.create_user(username='test2', password='12345')
        cls.user3 = User.objects.create_user(username='test3', password='12345')
        Follow.objects.add_follower(
            cls.user1,
            cls.user2,
        )
    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.post('/user/follow-add/',
                                    data={'path': reverse('profiles:detail', kwargs={'username': self.user2.username})})
        self.assertEqual(response.status_code, 302)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.post(reverse("users:follow-add"),
                                    data={'path': reverse('profiles:detail', kwargs={'username': self.user2.username})})
        self.assertEqual(response.status_code, 302)

    def test_not_logged(self):
        # test login requirement
        self.client.logout()
        response = self.client.post(reverse("users:follow-add"),
                                    data={'path': reverse('profiles:detail', kwargs={'username': self.user2.username})})
        self.assertRedirects(response, '/accounts/login/?next=/user/follow-add/')

    def test_post(self):
        # test post response

        # follow status before
        self.assertTrue(Follow.objects.follows(self.user1, self.user2))
        self.client.post(reverse("users:follow-add"),
                                     data={
                                         'path': reverse('profiles:detail', kwargs={'username': self.user2.username}),
                                         'status': 'is_followed',
                                         'username': self.user2.username,
                                     }
                                     )

        # follow status after unfollowing
        self.assertFalse(Follow.objects.follows(self.user1, self.user2))

        self.client.post(reverse("users:follow-add"),
                                     data={
                                         'path': reverse('profiles:detail', kwargs={'username': self.user2.username}),
                                         'status': 'not_followed',
                                         'username': self.user2.username,
                                     }
                                     )

        # follow status after following
        self.assertTrue(Follow.objects.follows(self.user1, self.user2))


class AdminTest(TestCase):
    '''
    Test registering models
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', password='12345', is_superuser=True, is_staff=True)

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_model(self):
        # test if model is registered
        response = self.client.get('/admin/restaurants/restaurant/')
        self.assertEqual(response.status_code, 200)


class RestaurantUserManagerTest(TestCase):
    '''
    Test RestaurantUserManager from users.models
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', city='Chorzów')
        cls.user2 = User.objects.create(username='user2')
        cls.rest1 = Restaurant.objects.create(name='verona', category='italian', owner=cls.user1, location='Katowice')
        cls.item1 = Item.objects.create(name='pizza', owner=cls.user1, restaurant=cls.rest1)

    def test_manager(self):

        # test manager's queryset response

        # empty query
        self.assertTrue(User.custom.search())
        self.assertEqual(User.custom.search().count(), 2)

        # query=username
        self.assertTrue(User.custom.search('test1', ['username', 'random']))
        self.assertTrue(User.custom.search('test', ['username', 'random']))

        # query=restaurant.name
        self.assertTrue(User.custom.search('verona', ['rest_name', 'random']))
        self.assertTrue(User.custom.search('ver', ['rest_name', 'random']))

        # query=restaurant.category
        self.assertTrue(User.custom.search('italian', ['rest_category', 'random']))
        self.assertTrue(User.custom.search('ital', ['rest_category', 'random']))

        # query=item
        self.assertTrue(User.custom.search('pizza', ['item', 'random']))
        self.assertTrue(User.custom.search('piz', ['item', 'random']))

        # query=item
        self.assertTrue(User.custom.search('Chor', ['city', 'random']))
        self.assertTrue(User.custom.search('Chorzów', ['city', 'random']))

        # query=restaurant.location
        self.assertTrue(User.custom.search('kato', ['rest_location', 'random']))
        self.assertTrue(User.custom.search('katowice', ['rest_location', 'random']))