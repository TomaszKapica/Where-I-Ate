from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.name, self.location)

    @property
    def title(self):
        return self.name


def r_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(r_pre_save_receiver, sender=Restaurant)