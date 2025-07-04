# Ficheiro: customers/admin.py (VERSÃO CORRIGIDA)

from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # O campo 'code' foi removido desta lista
    list_display = ('name', 'phone', 'email', 'city', 'state')
    
    # O campo 'code' também foi removido dos campos de busca
    search_fields = ('name', 'doc_number', 'phone', 'email')
    
    list_filter = ('city', 'state', 'created_at')