from django.urls import path, re_path
from .views import (
    ProfileListView,
    ProfileDetailView,
)


app_name = 'profiles'
urlpatterns = [
    path('search/', ProfileListView.as_view(), name='list'),
    re_path('(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='detail'),



]
