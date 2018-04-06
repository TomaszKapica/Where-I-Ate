from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Restaurant
from .forms import RestaurantCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from friendship.models import Follow
from menus.models import Item
from django.shortcuts import Http404, get_object_or_404
from django.urls import reverse_lazy


class MainPageView(TemplateView):
    '''
    View of main page
    '''
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'index.html', {})
        else:
            u_followings = [u.id for u in Follow.objects.following(request.user)]
            qs = list(Item.objects.filter(owner_id__in=u_followings))
            qs1 = list(Restaurant.objects.filter(owner_id__in=u_followings))
            qs.extend(qs1)

            try: # pragma: no cover
                import operator
            except ImportError: # pragma: no cover
                keyfun = lambda x: qs.updated  # use a lambda if no operator module
            else: # pragma: no cover
                keyfun = operator.attrgetter("updated")  # use operator since it's faster than lambda
            qs.sort(key=keyfun, reverse=True)

            limit = 10
            if len(qs) > limit: # pragma: no cover
                qs = qs[:limit-1]

            title = 'Recent Following Actions'
            return render(request, 'index-newest.html', {'qs': qs, 'title': title})


class ContactView(TemplateView):
    template_name = 'contact.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class RestaurantsListView(LoginRequiredMixin, ListView):
    '''
    View of all user's restaurants
    '''
    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    '''
    View creating restaurant
    '''

    form_class = RestaurantCreateForm
    template_name = 'form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    '''
    View updating restaurant
    '''

    form_class = RestaurantCreateForm
    template_name = 'restaurants/detail-update.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = 'Update {}'.format(name)
        return context

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


class RestaurantDeleteView(LoginRequiredMixin, DeleteView):
    '''
    View deleting restaurant
    '''

    success_url = reverse_lazy('restaurants:list')

    def get_object(self, queryset=None):
        rest_id = self.request.POST.get('id')
        return get_object_or_404(Restaurant.objects.filter(id__iexact=rest_id))
