from django.db import models # pragma: no cover
from django.conf import settings # pragma: no cover
from restaurants.models import Restaurant # pragma: no cover
from django.urls import reverse_lazy # pragma: no cover


class Item(models.Model):
    '''
    Item model
    fields:
    owner, restaurant, name, contents, excludes, timestamp, updated, public
    methods:
    get_contents, get_excludes, get_absolute_url, __str__
    '''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # pragma: no cover
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) # pragma: no cover
    name = models.CharField(max_length=150)# pragma: no cover
    contents = models.TextField(help_text='Separate each item by comma')# pragma: no cover
    excludes = models.TextField(blank=True, null=True, help_text='Separate each item by comma')# pragma: no cover
    timestamp = models.DateTimeField(auto_now_add=True) # pragma: no cover
    updated = models.DateTimeField(auto_now=True) # pragma: no cover
    public = models.BooleanField(default=True) # pragma: no cover

    class Meta: # pragma: no cover
        ordering = ['-updated', '-timestamp']

    def get_contents(self): # pragma: no cover
        return self.contents.split(',')

    def get_excludes(self): # pragma: no cover
        return self.excludes.split(',')

    def get_absolute_url(self): # pragma: no cover
        return reverse_lazy('menus:detail', kwargs={'pk': self.pk})

    def __str__(self): # pragma: no cover
        return self.name

