from django.test import TestCase
from restaurants.templatetags.rest_tags import sub_date
from datetime import datetime, timedelta


class RestTagTest(TestCase):
    '''
    Test rest_tags from restaurants/templatetags
    '''

    @classmethod
    def setUpTestData(cls):
        cls.date1 = datetime.now()
        cls.date2 = cls.date1
        cls.date3 = cls.date1 + timedelta(0, 1)

    def test_sub_date(self):

        # test sub_date templatetag return
        self.assertTrue(sub_date(self.date1, self.date2))
        self.assertFalse(sub_date(self.date1, self.date3))

