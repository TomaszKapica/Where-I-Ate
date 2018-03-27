from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item
from .forms import ItemForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import Http404, get_object_or_404


class ItemListView(ListView):
    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)


class ItemDetailView(DetailView):
    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
    form_class = ItemForm
    template_name = 'form.html'

    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Item'
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ItemForm
    template_name = 'menus/detail-update.html'

    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Item'
        return context

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('menus:list')

    def get_object(self, queryset=None):
        it_id = self.request.POST.get('id')
        if it_id is None:
            raise Http404
        return get_object_or_404(Item.objects.filter(id__iexact=it_id))
