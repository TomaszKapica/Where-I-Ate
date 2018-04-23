from rest_framework import serializers
from users.models import RestaurantUser
from api.restaurants.serializers import RestaurantReadSerializer


class ProfileSerializer(serializers.ModelSerializer):

    restaurant_set = RestaurantReadSerializer(many=True, read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = RestaurantUser
        fields = ('uri', 'pk', 'username', 'city', 'restaurant_set')
        read_only_fields = ('username', 'city')

    def get_uri(self, obj):
        request = self.context.get('request')
        return obj.get_absolute_uri(request)


