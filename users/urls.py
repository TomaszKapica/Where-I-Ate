from django.urls import path, re_path, include
from .views import (
    FriendListView,
    FriendToggleView,
    FollowToggleView,
    FriendshipRequestView,
    FollowListView
)


app_name = 'users'
urlpatterns = [
    path('', include('friendship.urls')),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('friend-add/', FriendToggleView.as_view(), name='friend-add'),
    path('follow-add/', FollowToggleView.as_view(), name='follow-add'),
    path('follow/', FollowListView.as_view(), name='follow-list'),
    path('requests/', FriendshipRequestView.as_view(), name='requests')





]
