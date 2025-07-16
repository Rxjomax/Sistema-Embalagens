# Ficheiro: production/models.py

from django.db import models
from django.conf import settings
from products.models import Product
from customers.models import Customer
from sales.models import Sale, SaleItem # 1. Importamos o SaleItem

class ProductionStage(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Estágio")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")

    class Meta:
        verbose_name = "Estágio de Produção"
        verbose_name_plural = "Estágios de Produção"
        ordering = ['order']

    def __str__(self):
        return self.name

class ProductionOrder(models.Model):
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Número da Ordem")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="production_orders", verbose_name="Produto")
    quantity = models.PositiveIntegerField(verbose_name="Quantidade")
    stage = models.ForeignKey(ProductionStage, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders", verbose_name="Estágio Atual")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True, related_name="production_orders", verbose_name="Venda de Origem")
    
    # ========================================================
    # ========= NOVO CAMPO ADICIONADO ABAIXO =========
    # ========================================================
    sale_item = models.OneToOneField(
        SaleItem, 
        on_delete=models.SET_NULL, # Usamos SET_NULL para não apagar a OP se o item for deletado
        null=True, 
        blank=True,
        related_name='production_order',
        verbose_name="Item da Venda de Origem"
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_orders", verbose_name="Criado por")
    notes = models.TextField(blank=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ordem de Produção"
        verbose_name_plural = "Ordens de Produção"
        ordering = ['-created_at']

    def __str__(self):
        return f"Ordem {self.order_number} - {self.product.name}"