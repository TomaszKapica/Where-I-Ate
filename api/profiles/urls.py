from django.urls import path, re_path
from .views import ProfilesListAPI, ProfilesRetrieveAPI

app_name = 'api_profiles'
urlpatterns = [
    path('', ProfilesListAPI.as_view(), name='list'),
    re_path('(?P<username>[\w-]+)/$', ProfilesRetrieveAPI.as_view(), name='detail'),


]