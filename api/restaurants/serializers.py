from rest_framework import serializers
from restaurants.models import Restaurant
from api.menus.serializers import MenusReadSerializer


class RestaurantSerializer(serializers.ModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('uri',
                  'owner',
                  'name',
                  'location',
                  'category',
                  'updated',
                  'timestamp')
        read_only_fields = ('owner',)

    def validate_name(self, value):

        qs = Restaurant.objects.filter(name__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Restaurant name already exists")

        return value

    def get_uri(self, obj):
        request = self.context['request']
        return obj.get_absolute_uri(request)


class RestaurantReadSerializer(serializers.ModelSerializer):

    item_set = MenusReadSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ('name',
                  'location',
                  'category',
                  'updated',
                  'timestamp',
                  'item_set'
                  )

        read_only_fields = fields
