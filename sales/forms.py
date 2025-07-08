# Ficheiro: sales/forms.py

from django import forms
from .models import Sale, SaleItem
from products.models import Product
from customers.models import Customer
from core.forms import RequiredFieldsMixin

class SaleForm(RequiredFieldsMixin, forms.ModelForm):
    customer_search = forms.CharField(
        label="Cliente", required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite para buscar um cliente...'})
    )
    class Meta:
        model = Sale
        fields = ['customer']
        widgets = {'customer': forms.HiddenInput()}
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('customer'):
            self.add_error('customer_search', "Você precisa selecionar um cliente válido da lista.")
        return cleaned_data

class SaleItemForm(forms.ModelForm):
    # Campo de busca que o usuário vê, mas que não é salvo diretamente
    product_search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control product-search-input',
            'placeholder': 'Buscar produto por nome ou código...'
        })
    )
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.HiddenInput(), # O campo real agora fica escondido
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': '1', 'value': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control price-input', 'readonly': 'readonly'}),
        }

SaleItemFormSet = forms.inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True
)