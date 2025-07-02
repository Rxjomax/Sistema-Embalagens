from django.urls import path
from .views import InventoryListView, create_stock_movement

app_name = 'inventory'

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory_list'),
    path('movimento/<str:movement_type>/', create_stock_movement, name='create_movement'),
]
