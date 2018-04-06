from django.views.generic import View, ListView
from friendship.models import Friend, Follow, FriendshipRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import RestaurantUser


class FriendListView(LoginRequiredMixin, ListView):
    '''
        View of user's friends
    '''

    template_name = 'users/friends-list.html'

    def get_queryset(self):
        return Friend.objects.friends(self.request.user)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        status = self.request.POST.get('status')
        path = self.request.POST.get('path')
        friend = RestaurantUser.objects.filter(username=username).first()
        logged_user = self.request.user
        if status == 'deleted':
            Friend.objects.remove_friend(logged_user, friend)
        return redirect(path)

    def get_context_data(self, *args, **kwargs):
        context = super(FriendListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'My Friends'
        return context


class FollowListView(LoginRequiredMixin, ListView):
    template_name = 'users/follow-list.html'

    def get_queryset(self):
        return Follow.objects.following(self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(FollowListView, self).get_context_data(*args, **kwargs)
        context['followed_by'] = Follow.objects.followers(self.request.user)
        context['title'] = 'Follow'
        context['title_1'] = 'My Followings'
        context['title_2'] = 'People following me'
        return context


class FriendToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        status = request.POST.get('status')
        path = request.POST.get('path')
        friend = RestaurantUser.objects.filter(username=username).first()
        current_user = request.user
        if status == 'not_friend':
            Friend.objects.add_friend(
                current_user,
                friend,
                message='I would like to be your friend.'
                )
        elif status == 'is_friend':
            Friend.objects.remove_friend(
                current_user,
                friend,
            )
        return redirect(path)


class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request,  *args, **kwargs):
        username = request.POST.get('username')
        status = request.POST.get('status')
        path = request.POST.get('path')
        logged_user = request.user
        followed = RestaurantUser.objects.filter(username=username).first()

        if status == 'not_followed':
            Follow.objects.add_follower(
                logged_user,
                followed,
                )
        elif status == 'is_followed':
            Follow.objects.remove_follower(
                logged_user,
                followed,
            )
        return redirect(path)


class FriendshipRequestView(LoginRequiredMixin, ListView):
    template_name = 'users/requests.html'

    def get_queryset(self):
        return Friend.objects.unrejected_requests(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(FriendshipRequestView, self).get_context_data(*args, **kwargs)
        context['sent_req'] = Friend.objects.sent_requests(user=self.request.user)
        context['title'] = 'Friendship Requests'
        context['title_1'] = 'Requested by'
        context['title_2'] = 'My Requests'
        return context

    def post(self, request, *args, **kwargs):
        req_id = request.POST.get('req_id')
        status = request.POST.get('status')
        path = request.POST.get('path')
        fr_obj = FriendshipRequest.objects.get(pk=req_id)
        if status == 'accepted':
            fr_obj.accept()
        elif status == 'rejected':
            fr_obj.reject()
        elif status == 'cancelled':
            fr_obj.cancel()
        return redirect(path)



