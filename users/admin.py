from django.contrib.auth.admin import UserAdmin
from .models import RestaurantUser
from django.contrib import admin


@admin.register(RestaurantUser)
class AdminRestaurantUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),

    )

