from django.db import models # pragma: no cover
from django.db.models.signals import pre_save # pragma: no cover
from .utils import unique_slug_generator # pragma: no cover
from django.conf import settings # pragma: no cover
from django.urls import reverse_lazy # pragma: no cover
from django.db.models import Q # pragma: no cover
from rest_framework.reverse import reverse as api_reverse

User = settings.AUTH_USER_MODEL


class RestaurantQuerySet(models.query.QuerySet):

    # search by name, location, category, restaurant's items
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(category__icontains=query) |
                Q(item__name__icontains=query) |
                Q(item__contents__icontains=query) |
                Q(name__iexact=query) |
                Q(location__iexact=query) |
                Q(category__iexact=query) |
                Q(item__name__iexact=query) |
                Q(item__contents__iexact=query)
            ).distinct()
        else:
            return self


class RestaurantManager(models.Manager):
    def get_queryset(self):
        return RestaurantQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Restaurant(models.Model):
    '''
    Restaurant model
    fields:
    owner, name, location, timestamp, updated, category, slug
    methods:
    title, get_absolute_url,
    '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # pragma: no cover
    name = models.CharField(max_length=150) # pragma: no cover
    location = models.CharField(max_length=150, null=True, blank=True) # pragma: no cover
    timestamp = models.DateTimeField(auto_now_add=True) # pragma: no cover
    updated = models.DateTimeField(auto_now=True) # pragma: no cover
    category = models.CharField(max_length=30) # pragma: no cover
    slug = models.SlugField(null=True, blank=True) # pragma: no cover
    objects = RestaurantManager()

    class Meta: # pragma: no cover
        ordering = ('-updated', '-timestamp')

    def __str__(self): # pragma: no cover
        return "{} {}".format(self.name, self.location)

    @property
    def title(self): # pragma: no cover
        return self.name

    def get_absolute_url(self): # pragma: no cover
        return reverse_lazy('restaurants:detail', kwargs={'slug': self.slug})

    def get_absolute_uri(self, request=None):
        return api_reverse('api_restaurants:rud', kwargs={'slug': self.slug}, request=request)


def r_pre_save_receiver(sender, instance, *args, **kwargs): # pragma: no cover
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(r_pre_save_receiver, sender=Restaurant) # pragma: no cover