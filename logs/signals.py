# Ficheiro: logs/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

# --- Importamos TODOS os modelos que queremos "escutar" ---
from products.models import Product
from categories.models import Category
from customers.models import Customer
from suppliers.models import Supplier
from sales.models import Sale
from finance.models import FinancialRecord

from .models import LogEntry
from .utils import get_current_user

# --- LOGS PARA PRODUTOS (Sem alterações) ---
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


# --- LOGS PARA CATEGORIAS (Sem alterações) ---
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


# ========================================================
# ========= LOGS PARA CLIENTES (CORRIGIDO) =========
# ========================================================
@receiver(post_save, sender=Customer)
def log_customer_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "CRIOU" if created else "ATUALIZOU"
    # MUDANÇA: Usamos o telefone (que é único) em vez do código
    description = f"O cliente '{instance.name}' (Telefone: {instance.phone}) foi {action.lower()}."
    LogEntry.objects.create(user=user, action=f"CLIENTE_{action}", description=description)

@receiver(post_delete, sender=Customer)
def log_customer_delete(sender, instance, **kwargs):
    user = get_current_user()
    action = "EXCLUSÃO"
    # MUDANÇA: Usamos o telefone (que é único) em vez do código
    description = f"O cliente '{instance.name}' (Telefone: {instance.phone}) foi EXCLUÍDO."
    LogEntry.objects.create(user=user, action="CLIENTE_EXCLUSÃO", description=description)


# --- LOGS PARA FORNECEDORES (Sem alterações) ---
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


# --- LOGS PARA USUÁRIOS (Sem alterações) ---
@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    user = get_current_user()
    if user is None or (created and user.is_anonymous):
        return
    action = "CRIOU" if created else "ATUALIZOU"
    description = f"O usuário '{instance.username}' foi {action.lower()}."
    LogEntry.objects.create(user=user, action=f"USUÁRIO_{action}", description=description)


# --- LOGS PARA VENDAS E REGISTROS FINANCEIROS (Sem alterações) ---
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
    if not created:
        action = "ATUALIZAÇÃO"
        description = f"O registro financeiro da Venda #{instance.sale.pk} foi atualizado (Status: {instance.get_status_display()})."
        LogEntry.objects.create(user=user, action=f"FINANCEIRO_{action}", description=description)