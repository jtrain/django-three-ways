from django.db.models import Count
from django.db.models.functions import Lower
from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, DetailView

from braces.views import (
    OrderableListMixin, FormValidMessageMixin, PrefetchRelatedMixin
)
from extra_views import (
    InlineFormSet, CreateWithInlinesView, SearchableListMixin
)

from lists.forms import ItemForm, ListForm
from lists.models import List, Item


class DashboardView(SearchableListMixin, PrefetchRelatedMixin,
                    OrderableListMixin, ListView):
    model = List
    prefetch_related = ['items']
    orderable_columns = ('created_at', 'lower_name', 'items_count')
    orderable_columns_default = '-created_at'
    search_fields = ['name', 'items__name']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            lower_name=Lower('name'),
            items_count=Count('items')
        )


class ItemsInline(InlineFormSet):
    model = Item
    form_class = ItemForm
    can_delete = False
    extra=30


class CreateNewList(FormValidMessageMixin, CreateWithInlinesView):
    model = List
    form_class = ListForm
    inlines = [ItemsInline]
    form_valid_message = _("List created!")


class DetailList(DetailView):
    model = List
