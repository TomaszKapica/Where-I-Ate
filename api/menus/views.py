from rest_framework import generics
from .serializers import MenusSerializer
from menus.models import Item
from django.db.models import Q


class ItemListCreateAPI(generics.ListCreateAPIView):

    serializer_class = MenusSerializer
    lookup_field = 'pk'

    def get_queryset(self):

        qs = Item.objects.filter(owner=self.request.user)
        item = self.request.GET.get('qs')
        if item is not None:
            qs = Item.objects.filter(
                Q(owner=self.request.user) &
                (
                        Q(name__iexact=item) |
                        Q(name__icontains=item)
                )
                                    )
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ItemRUDAPI(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = MenusSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user)