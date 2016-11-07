from django.utils.translation import ugettext as _

from rest_framework import viewsets
from rest_framework import mixins

from lists.models import List, Item
from lists.serializers import ListSerializer, ItemSerializer


class ListViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
