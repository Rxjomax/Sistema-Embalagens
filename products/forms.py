from django import forms
from .models import Product
from core.forms import RequiredFieldsMixin

class ProductForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Product
        # --- ORDEM DOS CAMPOS ATUALIZADA ---
        fields = ['name', 'code', 'category', 'unit_price', 'medida_x', 'medida_y', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'medida_x': forms.NumberInput(attrs={'class': 'form-control'}),
            'medida_y': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }