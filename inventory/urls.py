# Ficheiro: inventory/urls.py

from django.urls import path
from .views import InventoryListView, create_stock_movement

app_name = 'inventory'

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory_list'),
    
    # Rota de 'saida' removida. Mantemos apenas a de 'entrada'.
    path('registrar-entrada/', lambda request: create_stock_movement(request, 'entrada'), name='create_entry'),
]