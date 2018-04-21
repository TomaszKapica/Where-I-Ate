from django.urls import path, include

urlpatterns = [
    path('restaurants/', include('api.restaurants.urls')),
    path('items/', include('api.menus.urls')),
]



