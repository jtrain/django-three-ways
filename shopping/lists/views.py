from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, DetailView

from braces.views import (
    OrderableListMixin, FormValidMessageMixin, PrefetchRelatedMixin
)
from extra_views import InlineFormSet, CreateWithInlinesView

from lists.forms import ItemForm, ListForm
from lists.models import List, Item


class DashboardView(PrefetchRelatedMixin, OrderableListMixin, ListView):
    model = List
    prefetch_related = ['items']
    orderable_columns = ('created_at', 'name', 'quantity')
    orderable_columns_default = '-created_at'


class ItemsInline(InlineFormSet):
    model = Item
    form_class = ItemForm


class CreateNewList(FormValidMessageMixin, CreateWithInlinesView):
    model = List
    form_class = ListForm
    inlines = [ItemsInline]
    form_valid_message = _("List created!")


class DetailList(DetailView):
    model = List
