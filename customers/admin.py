from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'phone', 'city', 'state')
    search_fields = ('code', 'name', 'company_name', 'doc_number')
    list_filter = ('city', 'state')
