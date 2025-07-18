# Ficheiro: finance/urls.py

from django.urls import path
from .views import (
    FinancialRecordListView, 
    FinancialRecordUpdateView,
    ManageInstallmentView,
    monthly_report_view,
    archive_financial_record # 1. Importamos a nova view
)

app_name = 'finance'

urlpatterns = [
    path('', FinancialRecordListView.as_view(), name='record_list'),
    path('<int:pk>/gerir/', FinancialRecordUpdateView.as_view(), name='record_update'),
    
    # 2. NOVA ROTA para a ação de arquivar
    path('<int:pk>/arquivar/', archive_financial_record, name='record_archive'),

    path('installment/<int:pk>/manage/', ManageInstallmentView.as_view(), name='manage_installment'),
    path('relatorio-mensal/', monthly_report_view, name='monthly_report'),
]