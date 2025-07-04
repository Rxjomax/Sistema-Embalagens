# Ficheiro: logs/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

# --- 1. Importamos TODOS os modelos que queremos "escutar" ---
from products.models import Product
from categories.models import Category
from customers.models import Customer
from suppliers.models import Supplier
from sales.models import Sale
from finance.models import FinancialRecord

from .models import LogEntry
from .utils import get_current_user

# --- LOGS PARA PRODUTOS ---
@receiver(post_save, sender=Product)
def log_product_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "CRIOU" if created else "ATUALIZOU"
    description = f"O produto '{instance.name}' (Cód: {instance.code}) foi {action.lower()}."
    LogEntry.objects.create(user=user, action=f"PRODUTO_{action}", description=description)

@receiver(post_delete, sender=Product)
def log_product_delete(sender, instance, **kwargs):
    user = get_current_user()
    description = f"O produto '{instance.name}' (Cód: {instance.code}) foi EXCLUÍDO."
    LogEntry.objects.create(user=user, action="PRODUTO_EXCLUSÃO", description=description)


# --- LOGS PARA CATEGORIAS ---
@receiver(post_save, sender=Category)
def log_category_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "CRIOU" if created else "ATUALIZOU"
    description = f"A categoria '{instance.name}' (Cód: {instance.code}) foi {action.lower()}."
    LogEntry.objects.create(user=user, action=f"CATEGORIA_{action}", description=description)

@receiver(post_delete, sender=Category)
def log_category_delete(sender, instance, **kwargs):
    user = get_current_user()
    description = f"A categoria '{instance.name}' (Cód: {instance.code}) foi EXCLUÍDA."
    LogEntry.objects.create(user=user, action="CATEGORIA_EXCLUSÃO", description=description)


# --- LOGS PARA CLIENTES ---
@receiver(post_save, sender=Customer)
def log_customer_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "CRIOU" if created else "ATUALIZOU"
    description = f"O cliente '{instance.name}' (Cód: {instance.code}) foi {action.lower()}."
    LogEntry.objects.create(user=user, action=f"CLIENTE_{action}", description=description)

@receiver(post_delete, sender=Customer)
def log_customer_delete(sender, instance, **kwargs):
    user = get_current_user()
    description = f"O cliente '{instance.name}' (Cód: {instance.code}) foi EXCLUÍDO."
    LogEntry.objects.create(user=user, action="CLIENTE_EXCLUSÃO", description=description)


# --- LOGS PARA FORNECEDORES ---
@receiver(post_save, sender=Supplier)
def log_supplier_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "CRIOU" if created else "ATUALIZOU"
    description = f"O fornecedor '{instance.trade_name}' (Cód: {instance.code}) foi {action.lower()}."
    LogEntry.objects.create(user=user, action=f"FORNECEDOR_{action}", description=description)

@receiver(post_delete, sender=Supplier)
def log_supplier_delete(sender, instance, **kwargs):
    user = get_current_user()
    description = f"O fornecedor '{instance.trade_name}' (Cód: {instance.code}) foi EXCLUÍDO."
    LogEntry.objects.create(user=user, action="FORNECEDOR_EXCLUSÃO", description=description)


# --- LOGS PARA USUÁRIOS ---
@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    # Evita criar log quando a própria view já cria o usuário (para não duplicar)
    # E também quando o middleware de log ainda não pegou o usuário
    user = get_current_user()
    if user is None or (created and user.is_anonymous):
        return

    if created:
        action = "CRIAÇÃO"
        description = f"O usuário '{instance.username}' foi criado."
    else:
        action = "ATUALIZAÇÃO"
        description = f"O usuário '{instance.username}' foi atualizado."
    LogEntry.objects.create(user=user, action=f"USUÁRIO_{action}", description=description)


# --- LOGS PARA VENDAS E REGISTROS FINANCEIROS ---
@receiver(post_save, sender=Sale)
def log_sale_save(sender, instance, created, **kwargs):
    user = get_current_user()
    if created:
        action = "CRIAÇÃO"
        description = f"A Venda #{instance.pk} para o cliente '{instance.customer.name}' foi criada."
        LogEntry.objects.create(user=user, action=f"VENDA_{action}", description=description)

@receiver(post_save, sender=FinancialRecord)
def log_financial_record_update(sender, instance, created, **kwargs):
    user = get_current_user()
    # Só nos interessa a atualização (mudança de status, por exemplo)
    if not created:
        action = "ATUALIZAÇÃO"
        description = f"O registro financeiro da Venda #{instance.sale.pk} foi atualizado (Status: {instance.get_status_display()})."
        LogEntry.objects.create(user=user, action=f"FINANCEIRO_{action}", description=description)