# Ficheiro: sales/forms.py

from django import forms
from .models import Sale, SaleItem
from customers.models import Customer
from products.models import Product
from core.forms import RequiredFieldsMixin

class SaleForm(RequiredFieldsMixin, forms.ModelForm):
    customer_search = forms.CharField(
        label="Cliente", required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome ou telefone...',
            'autocomplete': 'off'
        })
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
    product_search = forms.CharField(
        label="", required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control product-search-input',
            'placeholder': 'Buscar por nome ou código...',
            'autocomplete': 'off'
        })
    )
    class Meta:
        model = SaleItem
        # --- CAMPOS DE COR ADICIONADOS À LISTA ---
        fields = ['product', 'quantity', 'unit_price', 'cor_embalagem', 'cor_logo_1', 'cor_logo_2']
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': '1', 'value': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control price-input', 'readonly': 'readonly'}),
            # Estilizando os novos campos de cor
            'cor_embalagem': forms.TextInput(attrs={'class': 'form-control color-input', 'placeholder': 'Ex: Kraft'}),
            'cor_logo_1': forms.TextInput(attrs={'class': 'form-control color-input', 'placeholder': 'Ex: Preto'}),
            'cor_logo_2': forms.TextInput(attrs={'class': 'form-control color-input', 'placeholder': 'Ex: Vermelho'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        if not self.cleaned_data.get('DELETE') and not cleaned_data.get('product'):
            self.add_error('product_search', 'Selecione um produto válido.')
        return cleaned_data

# CORRIGIDO: Removido min_num=1 para garantir que apenas uma linha apareça por padrão
SaleItemFormSet = forms.inlineformset_factory(
    Sale, SaleItem, form=SaleItemForm,
    extra=1,
    can_delete=True
)