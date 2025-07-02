from django import forms
from .models import StockMovement
from core.forms import RequiredFieldsMixin

class StockMovementForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'notes']
