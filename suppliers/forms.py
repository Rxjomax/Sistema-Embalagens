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
        # Adicionamos placeholders para guiar o utilizador
        widgets = {
            'cep': forms.TextInput(attrs={'placeholder': 'Digite o CEP e aguarde'}),
        }
