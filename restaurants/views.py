from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import Restaurant
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import RestaurantCreateForm
class MainPageView(TemplateView):
    template_name = 'index.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class AboutView(TemplateView):
    template_name = 'about.html'


index = MainPageView.as_view()
contact = ContactView.as_view()
about = AboutView.as_view()


class RestaurantsListView(ListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            queryset = Restaurant.objects.filter(Q(category__iexact=slug) | Q(category__contains=slug))
        else:
            queryset = Restaurant.objects.all()
        return queryset


search_restaurant = RestaurantsListView.as_view()


class RestaurantDetailView(DetailView):
    model = Restaurant


restaurant_detail = RestaurantDetailView.as_view()


class RestaurantCreateView(CreateView):
    form_class = RestaurantCreateForm
    template_name = 'restaurants/restaurant_create_form.html'
    success_url = '/restaurants/'


r_create = RestaurantCreateView.as_view()
