from django.db import models
from django.conf import settings
from restaurants.models import Restaurant
from django.urls import reverse_lazy


class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    contents = models.TextField(help_text='Separate each item by comma')
    excludes = models.TextField(blank=True, null=True, help_text='Separate each item by comma')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated', '-timestamp']

    def get_contents(self):
        print(self.contents)
        return self.contents.split(',')

    def get_excludes(self):
        return self.excludes.split(',')

    def get_absolute_url(self):
        return reverse_lazy('menus:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

