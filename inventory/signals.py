from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockMovement

@receiver(post_save, sender=StockMovement)
def update_stock_quantity(sender, instance, created, **kwargs):
    """
    Este sinal é acionado sempre que um StockMovement é guardado.
    Ele atualiza a quantidade em estoque do produto relacionado.
    """
    if created: # Executa apenas na criação de um novo movimento
        product = instance.product
        if instance.movement_type == 'ENTRADA':
            product.stock_quantity += instance.quantity
        elif instance.movement_type == 'SAIDA':
            product.stock_quantity -= instance.quantity
        # Poderíamos adicionar outras lógicas para 'AJUSTE', etc.
        
        product.save()
