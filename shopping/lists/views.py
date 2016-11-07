from django.utils.translation import ugettext as _
from django.views.generic import (
    ListView, CreateView, DetailView
)

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
    can_delete = False
    extra=30


class CreateNewList(FormValidMessageMixin, CreateWithInlinesView):
    model = List
    form_class = ListForm
    inlines = [ItemsInline]
    form_valid_message = _("List created!")

    def get_template_names(self):
        if getattr(self, 'object', None):
            return ['lists/list_detail.html']
        else:
            return super(CreateNewList, self).get_template_names()

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object = obj = form.save()
        for formset in inlines:
            formset.save()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        response['X-PJAX-URL'] = response['Location'] = obj.get_absolute_url()
        return response


class DetailList(DetailView):
    model = List
