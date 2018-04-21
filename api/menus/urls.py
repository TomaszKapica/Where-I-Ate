from django.urls import path, re_path
from .views import ItemListCreateAPI, ItemRUDAPI

app_name = 'api_items'
urlpatterns = [
    path('', ItemListCreateAPI.as_view(), name='list-create'),
    re_path('(?P<pk>\d+)/$', ItemRUDAPI.as_view(), name='rud'),


]