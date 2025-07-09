# Ficheiro: categories/forms.py

from django import forms
from .models import Category
from core.forms import RequiredFieldsMixin

class CategoryForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Category
        # --- ORDEM DOS CAMPOS ATUALIZADA ---
        fields = ['name', 'code']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }