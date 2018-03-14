from django.forms import ModelForm
from .models import Restaurant


class RestaurantCreateForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'location', 'category',
        ]

