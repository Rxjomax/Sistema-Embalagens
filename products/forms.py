from django import forms
from .models import Product
from core.forms import RequiredFieldsMixin  # 1. Importamos nossa nova ferramenta

# 2. Adicionamos o "RequiredFieldsMixin" à classe do formulário
class ProductForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'category', 'unit_price', 'medida_x', 'medida_y', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'medida_x': forms.NumberInput(attrs={'class': 'form-control'}),
            'medida_y': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }