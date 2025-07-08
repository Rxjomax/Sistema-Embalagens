# Ficheiro: sales/urls.py
from django.urls import path
from .views import SaleListView, SaleCreateView, customer_search_view, product_search_view

app_name = 'sales'

urlpatterns = [
    path('', SaleListView.as_view(), name='sale_list'),
    path('adicionar/', SaleCreateView.as_view(), name='sale_add'),
    
    path('api/search-customers/', customer_search_view, name='customer_search'),
    # NOVA ROTA PARA A API DE BUSCA DE PRODUTOS
    path('api/search-products/', product_search_view, name='product_search'),
]