from django.db import models

class Category(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

    # Esta propriedade vai contar quantos produtos usam esta categoria
    @property
    def product_count(self):
        return self.products.count()
