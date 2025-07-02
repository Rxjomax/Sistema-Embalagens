from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    import_products_view # Adicionar esta linha
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('adicionar/', ProductCreateView.as_view(), name='product_add'),
    path('<int:pk>/editar/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/excluir/', ProductDeleteView.as_view(), name='product_delete'),
    # ROTA DE IMPORTAÇÃO REINTRODUZIDA
    path('importar/', import_products_view, name='product_import'),
]
