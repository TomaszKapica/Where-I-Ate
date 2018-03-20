from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.shortcuts import Http404
from restaurants.models import Restaurant
from menus.models import Item
from django.db.models import Q

User = get_user_model()


class ProfileDetailView(DetailView):
    queryset = User.objects.filter(is_active=True)
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('qs')
        owner_qs = context['restaurantuser']
        item_qs = Item.objects.filter(owner=owner_qs)
        rest_qs = Restaurant.objects.filter(owner=owner_qs)
        if query:
            rest_qs = rest_qs.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(category__icontains=query)|
                Q(name__iexact=query)|
                Q(location__iexact=query)|
                Q(category__iexact=query)
            )
        if rest_qs.exists() and item_qs.exists():
            context['search_query'] = rest_qs
        return context

