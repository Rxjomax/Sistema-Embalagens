from django import forms
from .models import Customer
from core.forms import RequiredFieldsMixin

class CustomerForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'code', 'name', 'company_name', 'doc_number', 'email', 'phone',
            'cep', 'address', 'number', 'city', 'state'
        ]
        widgets = {
            'cep': forms.TextInput(attrs={'placeholder': 'Digite o CEP e aguarde'}),
        }
