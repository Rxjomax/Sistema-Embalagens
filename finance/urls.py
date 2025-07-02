# Ficheiro: finance/urls.py

from django.urls import path
from .views import (
    FinancialRecordListView, 
    FinancialRecordUpdateView,
    ManageInstallmentView # 1. Importamos a nova view do modal
)

app_name = 'finance'

urlpatterns = [
    path('', FinancialRecordListView.as_view(), name='record_list'),
    path('<int:pk>/gerir/', FinancialRecordUpdateView.as_view(), name='record_update'),

    # 2. NOVA ROTA para pegar e salvar os dados da parcela do modal
    path('installment/<int:pk>/manage/', ManageInstallmentView.as_view(), name='manage_installment'),
]