from django.db import models
from django.conf import settings
from products.models import Product

class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
        # No futuro, podemos adicionar 'VENDA', 'COMPRA', etc.
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    quantity = models.IntegerField(verbose_name="Quantidade Movimentada")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, verbose_name="Observações")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} de {self.quantity} para {self.product.name}"
