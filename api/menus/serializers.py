from rest_framework import serializers
from menus.models import Item
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant

User = get_user_model()


class MenusSerializer(serializers.ModelSerializer):

    uri = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(MenusSerializer, self).__init__(*args, **kwargs)
        self.fields['restaurant'].queryset = Restaurant.objects.filter(owner=self.context['request'].user)

    class Meta:

        model = Item
        fields = ('uri',
                  'owner',
                  'restaurant',
                  'name',
                  'contents',
                  'excludes',
                  'updated',
                  'timestamp',
                  'public')
        read_only_fields = ('owner',)

    def validate_name(self, value):

        restaurant = self.context['request'].data['restaurant']
        qs = Item.objects.filter(
            name__iexact=value,
            owner=self.context['request'].user,
            restaurant=restaurant,
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk, )

        if qs.exists():
            raise serializers.ValidationError('Item with this name already exists in restaurant')
        return value

    def get_uri(self, obj):
        request = self.context['request']
        return obj.get_absolute_uri(request)


class MenusReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('name',
                  'contents',
                  'excludes',
                  'updated',
                  'timestamp')

        read_only_fields = fields

