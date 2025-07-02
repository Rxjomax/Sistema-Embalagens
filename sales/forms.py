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
    # Usamos um campo especial para buscar produtos e mostrar o preço
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

# Criamos um FormSet que permite ter múltiplos SaleItemForms na mesma página
SaleItemFormSet = forms.inlineformset_factory(
    Sale, SaleItem, form=SaleItemForm,
    extra=1, can_delete=True, min_num=1
)
