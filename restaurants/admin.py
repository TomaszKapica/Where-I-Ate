from django.contrib import admin # pragma: no cover
from .models import Restaurant # pragma: no cover


@admin.register(Restaurant)# pragma: no cover
class RestaurantAdmin(admin.ModelAdmin):
    ordering = ('name', 'category', 'location')

