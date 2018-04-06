from django.contrib.auth.admin import UserAdmin # pragma: no cover
from .models import RestaurantUser # pragma: no cover
from django.contrib import admin # pragma: no cover


@admin.register(RestaurantUser) # pragma: no cover
class AdminRestaurantUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),

    )

