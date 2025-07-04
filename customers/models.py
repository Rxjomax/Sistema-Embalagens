# Ficheiro: customers/models.py

from django.db import models

class Customer(models.Model):
    # O campo 'code' foi removido.
    name = models.CharField(max_length=255, verbose_name="Nome / Nome Fantasia")
    
    company_name = models.CharField(max_length=255, blank=True, verbose_name="Razão Social")
    doc_number = models.CharField(max_length=18, blank=True, verbose_name="CPF ou CNPJ")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Telefone agora é o identificador único.
    phone = models.CharField(max_length=20, unique=True, verbose_name="Telefone")
    
    cep = models.CharField(max_length=9, verbose_name="CEP")
    address = models.CharField(max_length=255, verbose_name="Logradouro")
    number = models.CharField(max_length=20, verbose_name="Número")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="UF")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']

    def __str__(self):
        return self.name