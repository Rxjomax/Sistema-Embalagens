# Ficheiro: inventory/forms.py

from django import forms
from .models import StockMovement
from core.forms import RequiredFieldsMixin

class StockMovementForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = StockMovement
        # 1. Adicionamos o novo campo 'total_cost' à lista
        fields = ['product', 'quantity', 'total_cost', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 2. Loop para adicionar a classe a todos os campos
        for field_name, field in self.fields.items():
            if field_name == 'notes':
                field.widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
            else:
                # Garante que o placeholder correto seja adicionado ao campo de custo
                if field_name == 'total_cost':
                    field.widget.attrs.update({'class': 'form-control', 'placeholder': '0,00'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})