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
    path('create/', ItemCreateView.as_view(), name='create'),
    #re_path('(?P<pk>\d+)/edit/$', ItemUpdateView.as_view(), name='edit'),
    re_path('(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='detail'),




]
