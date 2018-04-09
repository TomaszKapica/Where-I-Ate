from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from restaurants.models import Restaurant
from menus.models import Item
from friendship.models import Friend, FriendshipRequest, Follow
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    '''
    Validates profile to view and search query
    '''
    queryset = User.objects.filter(is_active=True)
    template_name = 'profiles/profile_detail.html'

    # checks if viewed user exists
    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username__iexact=username)

    # checks search query
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('qs')
        owner_qs = context['restaurantuser']
        item_qs = Item.objects.filter(owner=owner_qs)
        rest_qs = Restaurant.objects.filter(owner=owner_qs).search(query)
        logged_user = self.request.user
        other_user = User.objects.filter(username=self.kwargs.get('username')).first()
        if logged_user != other_user:
            context['is_follower'] = Follow.objects.follows(logged_user, other_user)
            context['is_friend'] = Friend.objects.are_friends(logged_user, other_user)
            context['is_requested'] = FriendshipRequest.objects.filter(
                from_user=logged_user, to_user=other_user
            )

        if rest_qs.exists() and item_qs.exists():
            context['search_query'] = rest_qs
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    '''
    View to search profiles by username, location, restaurant's category, items
    '''
    template_name = 'profiles/profiles_list.html'

    queryset = User.objects.filter(is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('qs')
        events = list(self.request.GET.keys())[1:]
        if query:
            context['object_list'] = User.custom.search(query, events)
        context['title'] = 'Find Friends'
        return context
