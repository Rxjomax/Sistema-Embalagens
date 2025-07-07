# Ficheiro: sales/forms.py

from django import forms
from .models import Sale, SaleItem
from products.models import Product
from customers.models import Customer
from core.forms import RequiredFieldsMixin

class SaleForm(RequiredFieldsMixin, forms.ModelForm):
    # O campo de busca é apenas para a interface, não para validação
    customer_search = forms.CharField(
        label="Cliente",
        required=False, # MUDANÇA 1: Este campo não é mais obrigatório
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite para buscar um cliente...'
        })
    )

    class Meta:
        model = Sale
        # O campo 'customer' real é que será validado pelo Django
        fields = ['customer']
        widgets = {
            'customer': forms.HiddenInput(),
        }
    
    # MUDANÇA 2: Adicionamos uma validação customizada
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        
        # Se, após tudo, o campo 'customer' estiver vazio, nós geramos um erro
        if not customer:
            # O erro é associado ao campo visível (customer_search) para o usuário entender
            self.add_error('customer_search', "Você precisa selecionar um cliente válido da lista.")
            
        return cleaned_data

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

SaleItemFormSet = forms.inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True
)