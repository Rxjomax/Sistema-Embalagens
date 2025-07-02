from django.db import models

class Supplier(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    company_name = models.CharField(max_length=255, verbose_name="Razão Social")
    trade_name = models.CharField(max_length=255, blank=True, verbose_name="Nome Fantasia")
    doc_number = models.CharField(max_length=18, blank=True, verbose_name="CPF ou CNPJ")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    address = models.CharField(max_length=255, blank=True, verbose_name="Logradouro / Rua")
    number = models.CharField(max_length=20, blank=True, verbose_name="Número")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, blank=True, verbose_name="UF")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['company_name']

    def __str__(self):
        return self.company_name
