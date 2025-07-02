from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name="Utilizador")
    message = models.CharField(max_length=255, verbose_name="Mensagem")
    is_read = models.BooleanField(default=False, verbose_name="Lida")
    link = models.URLField(blank=True, null=True, verbose_name="Link")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-created_at']

    def __str__(self):
        return self.message
