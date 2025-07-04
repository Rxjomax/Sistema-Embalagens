# Ficheiro: sales/forms.py (VERSÃO SIMPLIFICADA)

from django import forms
from .models import Sale, SaleItem
from products.models import Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'})
        }

class SaleItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control product-selector'})
    )

    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': '1', 'value': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control price-input', 'readonly': 'readonly'}),
        }

# ================================================================
# ========= FORMSET SIMPLIFICADO ABAIXO =========
# ================================================================
SaleItemFormSet = forms.inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,  # Pede explicitamente UMA linha extra
    can_delete=True
    # O parâmetro min_num foi removido para eliminar qualquer conflito
)