from django.urls import path
from .views import (
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView
)

app_name = 'customers'

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('adicionar/', CustomerCreateView.as_view(), name='customer_add'),
    path('<int:pk>/editar/', CustomerUpdateView.as_view(), name='customer_update'),
    path('<int:pk>/excluir/', CustomerDeleteView.as_view(), name='customer_delete'),
]
