from django.db.models import Count
from django.db.models.functions import Lower
from django.utils.translation import ugettext as _

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import mixins

from lists.models import List, Item
from lists.serializers import ListSerializer, ItemSerializer


class ListViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'items__name')
    ordering_fields = ('lower_name', 'created_at', 'item_count')
    ordering = ('-created_at',)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            lower_name=Lower('name'),
            item_count=Count('items')
        )
