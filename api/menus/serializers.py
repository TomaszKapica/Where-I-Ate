from rest_framework import serializers
from menus.models import Item


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('owner', 'restaurant', 'name', 'contents', 'excludes', 'updated', 'timestamp', 'public')

