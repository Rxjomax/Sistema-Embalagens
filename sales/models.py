# Ficheiro: sales/models.py

from django.db import models
from django.conf import settings
from customers.models import Customer
from products.models import Product
from decimal import Decimal

class Sale(models.Model):
    STATUS_CHOICES = [
        ('EM_ABERTO', 'Em Aberto'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Cliente")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Vendedor")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Data da Venda")
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_ABERTO', verbose_name="Status")
    production_order_created = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-sale_date']

    def __str__(self):
        return f"Venda #{self.pk} - {self.customer.name}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE, verbose_name="Venda")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produto")
    quantity = models.PositiveIntegerField(verbose_name="Quantidade")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total do Item", default=0)

    # --- CAMPOS DE COR ADICIONADOS ---
    cor_embalagem = models.CharField(max_length=50, blank=True, verbose_name="Cor da Embalagem")
    cor_logo_1 = models.CharField(max_length=50, blank=True, verbose_name="Cor Logo 1")
    cor_logo_2 = models.CharField(max_length=50, blank=True, verbose_name="Cor Logo 2")

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"

    def save(self, *args, **kwargs):
        if self.unit_price and self.quantity:
            self.total = Decimal(self.unit_price) * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def get_total(self):
        if self.unit_price and self.quantity:
            return Decimal(self.unit_price) * Decimal(self.quantity)
        return Decimal('0.00')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"