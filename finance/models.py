# Ficheiro: finance/models.py

from django.db import models
from sales.models import Sale

class FinancialRecord(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('NAO_DEFINIDO', 'Não Definido'),
        ('A_VISTA', 'À Vista'),
        ('PARCELADO', 'Parcelado'),
        ('PIX', 'PIX'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('BOLETO', 'Boleto'),
    ]

    STATUS_CHOICES = [
        ('AGUARDANDO', 'Aguardando Pagamento'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]

    DELIVERY_STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGUE', 'Entregue'),
    ]

    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name="financial_record", verbose_name="Venda")
    
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        default='NAO_DEFINIDO', 
        verbose_name="Forma de Pagamento"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='AGUARDANDO', 
        verbose_name="Status Financeiro"
    )

    delivery_status = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS_CHOICES,
        default='PENDENTE',
        verbose_name="Status da Entrega"
    )

    installments = models.PositiveIntegerField(default=1, verbose_name="Número de Parcelas")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro Financeiro"
        verbose_name_plural = "Registros Financeiros"
        ordering = ['-created_at']

    def __str__(self):
        return f"Registro Financeiro para Venda #{self.sale.pk}"


class Installment(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADA', 'Atrasada'),
    ]

    financial_record = models.ForeignKey(
        FinancialRecord, 
        on_delete=models.CASCADE, 
        related_name="installments_list",
        verbose_name="Registro Financeiro"
    )
    
    installment_number = models.PositiveIntegerField(verbose_name="Número da Parcela")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Parcela")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")

    # ================================================================
    # ========= NOVOS CAMPOS ADICIONADOS ABAIXO =========
    # ================================================================
    paid_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Pago")
    paid_at = models.DateField(null=True, blank=True, verbose_name="Data de Pagamento")
    

    class Meta:
        verbose_name = "Parcela"
        verbose_name_plural = "Parcelas"
        unique_together = ('financial_record', 'installment_number')
        ordering = ['financial_record', 'installment_number']

    def __str__(self):
        return f"Parcela {self.installment_number} de Venda #{self.financial_record.sale.pk}"