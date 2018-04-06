from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item
from .forms import ItemForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import Http404, get_object_or_404


class ItemListView(LoginRequiredMixin, ListView):
    '''
    View of all owner items
    '''
    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
    '''
    View creating items
    '''
    form_class = ItemForm
    template_name = 'form.html'

    # adding user to form before saving
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    # passing user to limit restaurant choices in form __init__()
    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # passing title
    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Item'
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    '''
    View updating item
    '''
    form_class = ItemForm
    template_name = 'menus/detail-update.html'

    # all user items
    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)

    # passing title
    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Item'
        return context

    # passing user to limit restaurants choices
    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    '''
    View deleting item
    '''
    success_url = reverse_lazy('menus:list')

    # validating existence of item to delete
    def get_object(self, queryset=None):
        it_id = self.request.POST.get('id')
        return get_object_or_404(Item.objects.filter(id=it_id))
