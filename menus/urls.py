from django.urls import path, re_path
from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
)


app_name = 'menus'
urlpatterns = [
    path('', ItemListView.as_view(), name='list'),
    re_path('(?P<pk>\d+)/$', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/', ItemUpdateView.as_view(), name='update'),


]
