from django.contrib import admin
from .models import ProductionStage, ProductionOrder

@admin.register(ProductionStage)
class ProductionStageAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'product', 'quantity', 'stage', 'customer', 'created_at')
    list_filter = ('stage', 'customer', 'product')
    search_fields = ('order_number', 'product__name', 'customer__name')
