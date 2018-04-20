from rest_framework import serializers
from users.models import RestaurantUser


class RestaurantUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantUser
        fields = ('username', 'email', 'city', 'is_active', 'is_superuser')

