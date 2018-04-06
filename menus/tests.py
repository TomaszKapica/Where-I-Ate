from django.test import TestCase
from .models import Item
from restaurants.models import Restaurant
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class ItemModelTest(TestCase):
    '''
    Model Item Test
    methods:
    __str__ , get_contents, get_excludes, get_absolute_url
    '''

    @classmethod
    def setUpTestData(cls):
        cls.item = Item(name='Pizza', contents='olive,tomatoes,salami', excludes='garlic,chicken', public=True, id=1)

    def test_string_method(self):
        # test __str__()
        self.assertEqual(str(self.item), self.item.name)

    def test_get_contents(self):
        # test get_content()
        self.assertEqual(['olive', 'tomatoes', 'salami'], self.item.get_contents())

    def test_get_excludes(self):
        # test get_exclude()
        self.assertEqual(['garlic', 'chicken'], self.item.get_excludes())

    def test_get_absolute_url(self):
        # test correct redirect using get_absolute_url()
        self.assertEqual('/items/{}/'.format(self.item.id), self.item.get_absolute_url())

    def test_name_length_pass(self):
        # test length limit of name
        self.assertFalse(len(self.item.name) > self.item._meta.get_field('name').max_length)

    def test_contents_help_text(self):
        # test contents help_text attribute
        self.assertEqual(self.item._meta.get_field('contents').help_text, 'Separate each item by comma')

    def test_excludes_help_text(self):

        # test contents help_text attribute
        self.assertEqual(self.item._meta.get_field('excludes').help_text, 'Separate each item by comma')


class ItemListViewTest(TestCase):
    '''
    Tests ItemListView from menus.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.rest = Restaurant.objects.create(name='Ital', owner=cls.user1)
        cls.item = Item.objects.create(name='item1', owner=cls.user1, restaurant=cls.rest)

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse("menus:list"))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('menus:list'))
        self.assertRedirects(response, '/accounts/login/?next=/items/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse("menus:list"))
        self.assertTemplateUsed(response, 'menus/item_list.html')

    def test_get(self):

        # test get response
        response = self.client.get(reverse("menus:list"))
        obj = response.context['object_list']
        self.assertQuerysetEqual(obj, map(repr, Item.objects.filter(owner=self.user1)), ordered=False)


class ItemUpdateViewTest(TestCase):
    '''
    Tests ItemUpdateView from menus.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.rest = Restaurant.objects.create(name='Ital', owner=cls.user1)
        cls.item = Item.objects.create(name='item1', owner=cls.user1, restaurant=cls.rest, pk=0)

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/items/0/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(self.item.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(self.item.get_absolute_url())
        self.assertRedirects(response, '/accounts/login/?next=/items/0/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(self.item.get_absolute_url())
        self.assertTemplateUsed(response, 'menus/detail-update.html')

    def test_get(self):

        # test get response
        response = self.client.get(self.item.get_absolute_url())
        user = self.user1
        title = response.context['title']
        req_user = response.context['user']
        obj = response.context['object']

        self.assertEqual(title, 'Update Item')
        self.assertEqual(user, req_user)
        self.assertEqual(obj, Item.objects.filter(owner=user, id=self.item.id)[0])


class ItemDeleteViewTest(TestCase):
    '''
    Tests ItemDeleteView from menus.views
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')
        cls.rest = Restaurant.objects.create(name='Ital', owner=cls.user1)
        cls.item = Item.objects.create(name='item1', owner=cls.user1, restaurant=cls.rest, id=0)

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/items/delete')
        self.assertEqual(response.status_code, 301)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('menus:delete'))
        self.assertRedirects(response, '/accounts/login/?next=/items/delete/')

    def test_post(self):

        # test post response

        response = self.client.post(reverse('menus:delete'))

        # test delete of not existing object
        self.assertEqual(response.status_code, 404)

        # test if item exists
        self.assertTrue(Item.objects.filter(id=0))

        response1 = self.client.post(reverse('menus:delete'), data={'id': 500})

        # test delete item with not existing id
        self.assertEqual(response1.status_code, 404)

        response2 = self.client.post(reverse('menus:delete'), data={'id': 0})

        # test status after delete
        self.assertEqual(response2.status_code, 302)


        # test if deleted object doesn't exists
        self.assertFalse(Item.objects.filter(id=0))


class ItemCreateView(TestCase):
    '''
        Tests ItemCreateView from menus.views
        '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='test1', password='12345')

    def setUp(self):

        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_url_exists(self):

        # test if url path exists
        response = self.client.get('/items/create/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_name(self):

        # test if namespace:name is valid
        response = self.client.get(reverse('menus:create'))
        self.assertEqual(response.status_code, 200)

    def test_not_logged(self):

        # test login requirement
        self.client.logout()
        response = self.client.get(reverse('menus:create'))
        self.assertRedirects(response, '/accounts/login/?next=/items/create/')

    def test_correct_template(self):

        # test if template is valid
        response = self.client.get(reverse('menus:create'))
        self.assertTemplateUsed(response, 'form.html')

    def test_get(self):

        # test get response

        response = self.client.get(reverse('menus:create'))

        title = response.context['title']
        req_user = response.context['user']

        self.assertEqual(title, 'Add Item')
        self.assertEqual(self.user1, req_user)


class ItemFormTest(TestCase):
    '''
    Tests ItemForm from menus.forms
    '''

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='test1', password='12345')
        cls.rest = Restaurant.objects.create(name='Ital', owner=cls.user1)

    def setUp(self):
        self.client._login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[1])

    def test_valid_form_without_mandatory(self):

        # tests saving forms without all mandatory fields

        self.client.post(reverse('menus:create'), data={
            'restaurant': 1,
            'contents': 'olive, salami',
        }
                                    )

        self.assertFalse(Item.objects.all())

        self.client.post(reverse('menus:create'), data={
            'name': 'Pizza',
            'contents': 'olive, salami',
        }
                                    )

        self.assertFalse(Item.objects.all())

        self.client.post(reverse('menus:create'), data={
            'name': 'Pizza',
            'restaurant': 1,
        }
                                    )
        self.assertFalse(Item.objects.all())

    def test_valid_form_with_mandatory(self):

        # test saving form with all mandatory fields
        response = self.client.post(reverse('menus:create'), data={
                                                        'name': 'Pizza',
                                                        'restaurant': 1,
                                                        'contents': 'olive, salami',
                                                        }
                                    )

        self.assertTrue(Item.objects.all())
        self.assertEqual(Item.objects.all()[0].restaurant, self.rest)
        self.assertEqual(Item.objects.all()[0].owner, self.user1)


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
        response = self.client.get('/admin/menus/item/')
        self.assertEqual(response.status_code, 200)
