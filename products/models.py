# Ficheiro: products/models.py

from django.db import models
from categories.models import Category
from django.db.models import Max
from django.db.models.functions import Cast
from django.db.models import IntegerField

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Produto")
    
    # --- CAMPO DE CÓDIGO ATUALIZADO ---
    # Agora pode ser nulo e em branco, e não é único no nível do DB
    # para permitir a lógica de criação. A unicidade será garantida pelo código.
    code = models.CharField(
        max_length=50, 
        unique=True,
        blank=True, # Permite que o campo seja deixado em branco no admin/formulário
        verbose_name="Código"
    )
    
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário")
    stock_quantity = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")
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

    # --- LÓGICA DE AUTO-INCREMENTO ADICIONADA ---
    def save(self, *args, **kwargs):
        # Se o produto é novo (não tem ID) E o código não foi preenchido
        if not self.pk and not self.code:
            # Filtra apenas os códigos que são puramente numéricos
            numeric_codes = Product.objects.annotate(
                numeric_code=Cast('code', IntegerField())
            ).filter(numeric_code__isnull=False)
            
            # Encontra o maior valor numérico
            max_code = numeric_codes.aggregate(max_code=Max('numeric_code'))['max_code']
            
            # Define o próximo código
            if max_code is not None:
                self.code = str(max_code + 1)
            else:
                # Se não houver nenhum código numérico, começa do 1
                self.code = "1"
        
        super().save(*args, **kwargs)