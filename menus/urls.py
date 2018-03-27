from django.urls import path, re_path
from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
)


app_name = 'menus'
urlpatterns = [
    path('', ItemListView.as_view(), name='list'),
    path('create/', ItemCreateView.as_view(), name='create'),
    #re_path('(?P<pk>\d+)/edit/$', ItemUpdateView.as_view(), name='edit'),
    path('delete/', ItemDeleteView.as_view(), name='delete'),
    re_path('(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='detail'),




]
