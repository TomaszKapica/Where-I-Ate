from django.contrib.auth.models import AbstractUser, BaseUserManager # pragma: no cover
from django.db import models
from django.db.models import Q
from functools import reduce
import operator
from rest_framework.reverse import reverse as api_reverse


class RestaurantUserQueryset(models.query.QuerySet):

    def search(self, query=None, events=None):
        filters = []
        if query and events:
            if 'rest_name' in events:
                filters.append(('restaurant__name__icontains', query))
                filters.append(('restaurant__name__iexact', query))
            if 'rest_category' in events:
                filters.append(('restaurant__category__icontains', query))
                filters.append(('restaurant__category__iexact', query))
            if 'item' in events:
                filters.append(('item__name__icontains', query))
                filters.append(('item__name__iexact', query))
            if 'username' in events:
                filters.append(('username__icontains', query))
                filters.append(('username__iexact', query))
            if 'city' in events:
                filters.append(('city__icontains', query))
                filters.append(('city__iexact', query))
            if 'rest_location' in events:
                filters.append(('restaurant__location__icontains', query))
                filters.append(('restaurant__location__iexact', query))

            filters = [Q(x) for x in filters]
            return self.filter(reduce(operator.or_, filters)).distinct()
        else:
            return self


class RestaurantUserManager(BaseUserManager):

    def get_queryset(self):
        return RestaurantUserQueryset(self.model, using=self.db)

    def search(self, query=None, events=None):
        return self.get_queryset().filter(is_active=True).search(query, events)


class RestaurantUser(AbstractUser): # pragma: no cover
    # RestaurantUser model
    city = models.TextField(max_length=150, null=True, blank=True)
    custom = RestaurantUserManager()

    def get_absolute_uri(self, request=None):
        return api_reverse('api_profiles:detail', kwargs={'username': self.username}, request=request)




