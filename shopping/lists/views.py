from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView, DetailView

from braces.views import OrderableListMixin, FormValidMessageMixin

from lists.models import List


class DashboardView(OrderableListMixin, ListView):
    model = List
    orderable_columns = ('created_at', 'name', 'quantity')
    orderable_columns_default = '-created_at'


class CreateNewList(FormValidMessageMixin, CreateView):
    model = List
    fields = ('name', 'items')
    form_valid_message = _("List created!")


class DetailList(DetailView):
    model = List
