# Ficheiro: finance/forms.py (VERSÃO SIMPLIFICADA)

from django import forms
from .models import FinancialRecord, Installment

class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ['payment_method', 'status', 'delivery_status', 'installments']

class InstallmentForm(forms.ModelForm):
    # Deixamos este formulário o mais simples possível
    class Meta:
        model = Installment
        fields = ['due_date', 'paid_value', 'paid_at', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'paid_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'paid_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }