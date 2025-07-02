# Ficheiro: production/forms.py

from django import forms
from .models import ProductionStage, ProductionOrder

class ProductionStageForm(forms.ModelForm):
    class Meta:
        model = ProductionStage
        fields = ['name', 'order']
        labels = {
            'name': 'Nome do Estágio',
            'order': 'Ordem de Exibição (menor aparece primeiro)',
        }

class ProductionOrderForm(forms.ModelForm):
    class Meta:
        model = ProductionOrder
        fields = ['order_number', 'product', 'quantity', 'stage', 'customer', 'notes']