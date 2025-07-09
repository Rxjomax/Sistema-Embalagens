# Ficheiro: customers/forms.py

from django import forms
from .models import Customer
from core.forms import RequiredFieldsMixin

class CustomerForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Customer
        # --- ORDEM DOS CAMPOS ATUALIZADA ---
        fields = [
            'name', 'phone', 'email', 'doc_number', 'company_name',
            'cep', 'address', 'number', 'city', 'state'
        ]
        widgets = {
            # O loop foi substituído pela definição explícita para garantir a ordem
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'doc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CEP e aguarde'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }