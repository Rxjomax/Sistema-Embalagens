# Ficheiro: finance/forms.py (VERSÃO CORRIGIDA)

from django import forms
from .models import FinancialRecord, Installment
import datetime  # <-- 1. IMPORTAÇÃO QUE FALTAVA ADICIONADA AQUI

# Formulário para os dados gerais do registro financeiro
class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ['payment_method', 'status', 'delivery_status', 'installments']

# Formulário para UMA ÚNICA parcela, usado no modal de edição
class InstallmentForm(forms.ModelForm):
    class Meta:
        model = Installment
        fields = ['due_date', 'paid_value', 'paid_at', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'paid_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'paid_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

# ================================================================
# ========= FORMULÁRIO PARA O FILTRO DO RELATÓRIO MENSAL =========
# ================================================================
class MonthlyReportForm(forms.Form):
    # Gera uma lista de anos (do ano atual até 5 anos atrás)
    YEAR_CHOICES = [(y, y) for y in range(datetime.date.today().year, datetime.date.today().year - 6, -1)]
    
    # Gera uma lista de meses
    MONTH_CHOICES = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]

    year = forms.ChoiceField(choices=YEAR_CHOICES, label="Ano")
    month = forms.ChoiceField(choices=MONTH_CHOICES, label="Mês")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona a classe de estilo aos campos do formulário
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'