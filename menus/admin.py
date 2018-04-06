from django.contrib import admin #pragma : no cover
from .models import Item #pragma : no cover


@admin.register(Item) # pragma: no cover
class AdminItem(admin.ModelAdmin):
    ordering = ['restaurant', 'name', 'owner']
