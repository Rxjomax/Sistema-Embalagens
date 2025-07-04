# Ficheiro: logs/models.py
from django.db import models
from django.conf import settings

class LogEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    action = models.CharField(max_length=50)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Registro de Log"
        verbose_name_plural = "Registros de Logs"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"