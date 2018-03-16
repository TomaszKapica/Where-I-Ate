from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Item
from .forms import ItemForm


class ItemListView(ListView):
    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)


class ItemDetailView(DetailView):
    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)


class ItemCreateView(CreateView):
    form_class = ItemForm
    template_name = 'form.html'

    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Add Item'
        return context


class ItemUpdateView(UpdateView):
    form_class = ItemForm

    def get_queryset(self):
        return Item.objects.all().filter(owner=self.request.user)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(ItemUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Item'
        return context
