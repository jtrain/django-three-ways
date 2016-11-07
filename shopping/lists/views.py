from django.utils.translation import ugettext as _

from rest_framework import viewsets
from lists.models import List, Item


class ListViewSet(viewsets.ModelViewSet):
    model = List
