from django import forms

from lists.models import List, Item


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']
        widgets = {
            'name': forms.TextInput()
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput()
        }
