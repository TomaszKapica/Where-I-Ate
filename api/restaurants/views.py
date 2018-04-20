from api.restaurants.serializers import RestaurantSerializer
from restaurants.models import Restaurant
from rest_framework import generics
from django.contrib.auth import get_user_model


User = get_user_model()


class RestaurantListCreateAPI(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Restaurant.objects.filter(owner=self.request.user)
        q = self.request.GET.get('qs')
        if q is not None:
            qs = Restaurant.objects.search(q)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantRUDAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)






