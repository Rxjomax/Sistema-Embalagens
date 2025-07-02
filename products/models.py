# Ficheiro: products/models.py (VERSÃO ATUALIZADA)

from django.db import models
from categories.models import Category

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Produto")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário")
    
    stock_quantity = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")
    
    # ================================================================
    # ========= NOVO CAMPO ADICIONADO ABAIXO =========
    # ================================================================
    minimum_stock = models.PositiveIntegerField(
        default=0, 
        verbose_name="Estoque Mínimo",
        help_text="Quando o estoque atual atingir ou ficar abaixo deste valor, um alerta será gerado."
    )

    medida_x = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Medida X")
    medida_y = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Medida Y")
    description = models.TextField(blank=True, verbose_name="Descrição (Marketing)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['name']

    def __str__(self):
        return self.name