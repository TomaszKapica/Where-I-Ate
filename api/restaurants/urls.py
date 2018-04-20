from django.urls import path, re_path
from .views import RestaurantListCreateAPI, RestaurantRUDAPI

app_name = 'api_restaurants'
urlpatterns = [
    path('', RestaurantListCreateAPI.as_view(), name='list-create'),
    re_path('(?P<slug>[\w-]+)/$', RestaurantRUDAPI.as_view(), name='rud'),


]