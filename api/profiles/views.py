from rest_framework import generics, response
from rest_framework.permissions import AllowAny
from .serializers import ProfileSerializer
from users.models import RestaurantUser
from restaurants.models import Restaurant
from menus.models import Item
import itertools


class ProfilesListAPI(generics.ListAPIView):

    '''
            View displaying all user profiles, visible to everyone
    '''

    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):

        profiles = RestaurantUser.objects.filter(is_active=True)
        qs = self.request.GET.get('qs')
        if qs:
            events = list(self.request.GET.keys())[1:]
            profiles = RestaurantUser.custom.search(query=qs, events=events)

        return profiles

    def list(self, request, *args, **kwargs):

        # adding restaurant_count, item_count, restaurant_categories to serialized data
        # erasing restaurant_set from data
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        new_serialized = []
        for x in serializer.data:
            x['restaurant_count'] = len(x['restaurant_set'])
            categories = (Restaurant.objects.filter(owner__pk=x['pk']).values_list('category'))
            x['restaurant_categories'] = list(set(itertools.chain(*categories)))
            x['item_count'] = Item.objects.filter(owner__pk=x['pk']).count()
            del x['restaurant_set']
            new_serialized.append(x)

        return response.Response(new_serialized)


class ProfilesRetrieveAPI(generics.RetrieveAPIView):

    '''
    View displaying retrieved profile, profile's restaurants and items
    '''
    serializer_class = ProfileSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return RestaurantUser.objects.filter(is_active=True)

