from django import forms

from lists.models import List, Item


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']
