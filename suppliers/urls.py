from django.urls import path
from .views import (
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView
)

app_name = 'suppliers'

urlpatterns = [
    path('', SupplierListView.as_view(), name='supplier_list'),
    path('adicionar/', SupplierCreateView.as_view(), name='supplier_add'),
    path('<int:pk>/editar/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('<int:pk>/excluir/', SupplierDeleteView.as_view(), name='supplier_delete'),
]
