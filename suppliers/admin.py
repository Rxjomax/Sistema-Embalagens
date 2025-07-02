from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('code', 'company_name', 'trade_name', 'phone', 'city', 'state')
    search_fields = ('code', 'company_name', 'trade_name', 'doc_number')
    list_filter = ('city', 'state')
