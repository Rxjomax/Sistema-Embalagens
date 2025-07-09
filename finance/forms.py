# Ficheiro: finance/forms.py

from django import forms
from .models import FinancialRecord, Installment
import datetime
from core.forms import RequiredFieldsMixin # Supondo que você o tenha em core/forms.py

class FinancialRecordForm(RequiredFieldsMixin, forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ['payment_method', 'status', 'delivery_status', 'installments']

    # Adiciona a classe de estilo a todos os campos do formulário
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class InstallmentForm(forms.ModelForm):
    # (Seu InstallmentForm existente, sem alterações)
    class Meta:
        model = Installment
        fields = ['due_date', 'paid_value', 'paid_at', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'paid_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'paid_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class MonthlyReportForm(forms.Form):
    # (Seu MonthlyReportForm existente, sem alterações)
    YEAR_CHOICES = [(y, y) for y in range(datetime.date.today().year, datetime.date.today().year - 6, -1)]
    MONTH_CHOICES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]
    year = forms.ChoiceField(choices=YEAR_CHOICES, label="Ano")
    month = forms.ChoiceField(choices=MONTH_CHOICES, label="Mês")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'