# Ficheiro: suppliers/forms.py

from django import forms
from .models import Supplier
from core.forms import RequiredFieldsMixin

class SupplierForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'code', 'company_name', 'trade_name', 'doc_number', 'phone',
            'cep', 'address', 'number', 'city', 'state'
        ]
        
        # ================================================================
        # ========= WIDGETS ATUALIZADOS PARA TODOS OS CAMPOS =========
        # ================================================================
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'trade_name': forms.TextInput(attrs={'class': 'form-control'}),
            'doc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CEP e aguarde'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }