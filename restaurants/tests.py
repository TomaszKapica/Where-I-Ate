from django.test import TestCase
from django.conf import settings
from .models import Restaurant
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from friendship.models import Follow
from menus.models import Item
from .forms import RestaurantCreateForm

User = get_user_model()


class RestaurantModelTest(TestCase):
    '''
    Model Item Test
    methods:
    __str__ , get_contents, get_excludes, get_absolute_url
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test', password='12345')
        cls.rest = Restaurant.objects.create(name='Italiana', id=1, owner=cls.user)
        cls.rest1 = Restaurant.objects.create(name='Tacos', id=2, owner=cls.user)

        cls.rest.save()

    def test_string_method(self):
        # test __str__()
        self.assertEqual(str(self.rest), "{} {}".format(self.rest.name, self.rest.location), )

    def test_get_absolute_url(self):
        # test correct redirect using get_absolute_url()
        self.assertTrue(self.rest.slug)
        self.assertEqual('/restaurants/{}/'.format(self.rest.slug), self.rest.get_absolute_url())

    def test_name_length_pass(self):
        # test length limit of name
        self.assertFalse(len(self.rest.name) > self.rest._meta.get_field('name').max_length)

    def test_title(self):
        self.assertEqual(self.rest.title, self.rest.name)

    def test_restaurant_manager(self):

        self.assertEqual({self.rest, self.rest1}, set(Restaurant.objects.search('')))

        self.assertEqual({self.rest}, set(Restaurant.objects.search('it')))

        self.assertEqual({self.rest, self.rest1}, set(Restaurant.objects.search('ta')))


class MainPageViewTest(TestCase):
    '''
    Tests MainPageView from restaurants.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345', is_active=True)
        cls.user2 = User.objects.create_user(username='test2', password='12345', is_active=True)
        cls.rest1 = Restaurant.objects.create(name='Ital', owner=cls.user2)
        cls.rest2 = Restaurant.objects.create(name='PancakePlace', owner=cls.user2)
        Follow.objects.add_follower(cls.user1, cls.user2)

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index-newest.html')

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get(self):

        # test get response
        response = self.client.get(reverse('home'))
        qs = response.context['qs']
        title = response.context['title']

        self.assertTrue(len(qs) <= 10)
        self.assertTrue(title)
        self.assertEqual(title, 'Recent Following Actions')


class AboutViewTest(TestCase):
    '''
    Tests AboutView from restaurants.views
    '''

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, 'about.html')


class ContactViewTest(TestCase):
    '''
    Tests ContactView from restaurants.views
    '''

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response, 'contact.html')


class RestaurantListViewTest(TestCase):
    '''
    Tests RestaurantListView from restaurants.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.rest = Restaurant.objects.create(name='Ital', owner=cls.user1)

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/restaurants/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse("restaurants:list"))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('restaurants:list'))
        self.assertRedirects(response, '/accounts/login/?next=/restaurants/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse("restaurants:list"))
        self.assertTemplateUsed(response, 'restaurants/restaurant_list.html')

    def test_get(self):

        # test get response
        response = self.client.get(reverse("restaurants:list"))
        obj = response.context['object_list']
        self.assertQuerysetEqual(obj, map(repr, Restaurant.objects.filter(owner=self.user1)), ordered=False)


class RestaurantUpdateViewTest(TestCase):
    '''
    Tests RestaurantUpdateView from restaurants.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.rest = Restaurant.objects.create(name='Ital', owner=cls.user1)

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/restaurants/ital/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(self.rest.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(self.rest.get_absolute_url())
        self.assertRedirects(response, '/accounts/login/?next=/restaurants/ital/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(self.rest.get_absolute_url())
        self.assertTemplateUsed(response, 'restaurants/detail-update.html')

    def test_get(self):

        # test get response
        response = self.client.get(self.rest.get_absolute_url())
        title = response.context['title']
        obj = response.context['object']

        self.assertEqual(title, 'Update Ital')
        self.assertEqual(obj, Restaurant.objects.filter(owner=self.user1, id=self.rest.id)[0])


class RestaurantDeleteViewTest(TestCase):
    '''
    Tests RestaurantDeleteView from restaurants.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.rest = Restaurant.objects.create(name='Ital', owner=cls.user1, id=0)
        cls.item = Item.objects.create(name='item1', owner=cls.user1, restaurant=cls.rest, id=0)

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/restaurants/delete')
        self.assertEqual(response.status_code, 301)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('restaurants:delete'))
        self.assertRedirects(response, '/accounts/login/?next=/restaurants/delete/')

    def test_post(self):

        # test post response

        response = self.client.post(reverse('restaurants:delete'))

        # test delete of not existing object
        self.assertEqual(response.status_code, 404)

        # test if item exists
        self.assertTrue(Restaurant.objects.filter(id=0))

        response1 = self.client.post(reverse('restaurants:delete'), data={'id': 500})

        # test delete item with not existing id
        self.assertEqual(response1.status_code, 404)

        response2 = self.client.post(reverse('restaurants:delete'), data={'id': 0})

        # test status after delete
        self.assertEqual(response2.status_code, 302)

        # test if deleted restaurant and it's item exist
        self.assertFalse(Restaurant.objects.filter(id=0))
        self.assertFalse(Item.objects.filter(id=0))


class RestaurantCreateView(TestCase):
    '''
        Tests RestaurantCreateView from restaurants.views
        '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/restaurants/create/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse('restaurants:create'))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('restaurants:create'))
        self.assertRedirects(response, '/accounts/login/?next=/restaurants/create/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse('restaurants:create'))
        self.assertTemplateUsed(response, 'form.html')

    def test_post(self):

        # test post response

        response = self.client.get(reverse('restaurants:create'))
        title = response.context['title']

        self.assertEqual(title, 'Add Restaurant')


class RestaurantCreateFormTest(TestCase):
    '''
    Tests RestaurantCreateForm from restaurants.forms
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', password='12345')

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_valid_form_without_mandatory(self):

        # test form without all mandatory fields
        form = RestaurantCreateForm({'category': 'Italian'})
        self.assertFalse(form.is_valid())
        form = RestaurantCreateForm({'name': 'Italiana'})
        self.assertFalse(form.is_valid())

    def test_valid_form_with_mandatory(self):

        # test form with all mandatory fields

        form = RestaurantCreateForm({'name': 'Italiana', 'category': 'Italian'})
        self.assertTrue(form.is_valid())

        self.client.post(reverse('restaurants:create'), data={
            'name': 'Italiana',
            'category': 'Italian'
        }
                                    )

        self.assertTrue(Restaurant.objects.all())
        self.assertEqual(Restaurant.objects.all()[0].owner, self.user1)


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






