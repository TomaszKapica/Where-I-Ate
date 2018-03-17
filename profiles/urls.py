from django.urls import path, re_path
from .views import (
    ProfileDetailView,
)


app_name = 'profiles'
urlpatterns = [
    re_path('(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='detail'),



]
