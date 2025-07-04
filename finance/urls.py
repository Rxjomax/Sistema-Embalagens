# Ficheiro: finance/urls.py

from django.urls import path
from .views import (
    FinancialRecordListView, 
    FinancialRecordUpdateView,
    ManageInstallmentView,
    monthly_report_view # 1. Importamos a nova view do relatório
)

app_name = 'finance'

urlpatterns = [
    path('', FinancialRecordListView.as_view(), name='record_list'),
    path('<int:pk>/gerir/', FinancialRecordUpdateView.as_view(), name='record_update'),
    path('installment/<int:pk>/manage/', ManageInstallmentView.as_view(), name='manage_installment'),
    
    # 2. NOVA ROTA para a página de relatório
    path('relatorio-mensal/', monthly_report_view, name='monthly_report'),
]