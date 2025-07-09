# Ficheiro: inventory/models.py

from django.db import models
from django.conf import settings
from products.models import Product

class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    quantity = models.IntegerField(verbose_name="Quantidade Movimentada")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    
    # --- NOVO CAMPO ADICIONADO ---
    # Este campo guardará o custo total da entrada de estoque
    total_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Custo Total da Entrada"
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, verbose_name="Observações")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} de {self.quantity} para {self.product.name}"