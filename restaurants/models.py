from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models import Q

User = settings.AUTH_USER_MODEL


class RestaurantQuerySet(models.query.QuerySet):
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
                Q(category__iexact=query)|
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
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)
    objects = RestaurantManager()

    class Meta:
        ordering = ('-updated', '-timestamp')

    def __str__(self):
        return "{} {}".format(self.name, self.location)

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('restaurants:detail', kwargs={'slug': self.slug})


def r_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(r_pre_save_receiver, sender=Restaurant)