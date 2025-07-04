# Ficheiro: logs/admin.py

from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Configuração para exibir os registros de log na área de administração.
    """
    list_display = ('timestamp', 'user', 'action', 'description')
    list_filter = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'description')
    
    # --- Configuração de Segurança ---
    # Transforma a área de logs em um local de apenas leitura.
    # Isso é muito importante para garantir a integridade da sua trilha de auditoria.
    
    def has_add_permission(self, request):
        # Ninguém pode adicionar um log manualmente.
        return False

    def has_change_permission(self, request, obj=None):
        # Ninguém pode alterar um log existente.
        return False

    def has_delete_permission(self, request, obj=None):
        # Ninguém pode deletar um log.
        return False