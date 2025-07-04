# Ficheiro: customers/forms.py

from django import forms
from .models import Customer
from core.forms import RequiredFieldsMixin

class CustomerForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Customer
        # 'code' foi removido desta lista
        fields = [
            'name', 'company_name', 'doc_number', 'email',
            'phone', 'cep', 'address', 'number', 'city', 'state'
        ]
        # Adiciona a classe CSS para estilização
        widgets = {
            field_name: forms.TextInput(attrs={'class': 'form-control'})
            for field_name in fields
        }
        widgets['email'] = forms.EmailInput(attrs={'class': 'form-control'})
        widgets['cep'] = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CEP e aguarde'})