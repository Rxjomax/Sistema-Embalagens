from django.contrib import admin
from .models import Product

# A importação de 'SubCategory' foi removida.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # A referência a 'subcategory' foi removida de todas as listas.
    list_display = ('name', 'code', 'category', 'unit_price')
    search_fields = ('name', 'code')
    list_filter = ('category',)
    # O Django é suficientemente inteligente para criar um bom widget de seleção para a categoria.
    # autocomplete_fields é mais útil quando há centenas de opções.
    # Vamos manter simples por agora.
