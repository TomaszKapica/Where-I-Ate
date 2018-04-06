from django.forms import ModelForm
from .models import Restaurant


class RestaurantCreateForm(ModelForm):
    # RestaurantForm
    class Meta:
        model = Restaurant
        fields = [
            'name', 'location', 'category',
        ]

