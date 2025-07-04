# Ficheiro: customers/urls.py (VERSÃO ATUALIZADA)

from django.urls import path
from .views import (
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    import_customers_view # 1. Importamos a nova view
)

app_name = 'customers'

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('adicionar/', CustomerCreateView.as_view(), name='customer_add'),
    path('<int:pk>/editar/', CustomerUpdateView.as_view(), name='customer_update'),
    path('<int:pk>/excluir/', CustomerDeleteView.as_view(), name='customer_delete'),

    # 2. Adicionamos a nova rota para a página de importação
    path('importar/', import_customers_view, name='customer_import'),
]