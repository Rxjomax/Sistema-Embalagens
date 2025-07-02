# Ficheiro: sales/urls.py

from django.urls import path
from .views import SaleListView, SaleCreateView

app_name = 'sales'

urlpatterns = [
    path('', SaleListView.as_view(), name='sale_list'),
    path('nova/', SaleCreateView.as_view(), name='sale_add'),
]