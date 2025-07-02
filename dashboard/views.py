# Ficheiro: dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Q, F # 1. Importamos o "F" para comparar campos do modelo
from datetime import timedelta

from customers.models import Customer
from products.models import Product
from finance.models import FinancialRecord
from inventory.models import StockMovement

@login_required
def dashboard_view(request):
    # --- Cálculos para os Cards (existentes) ---
    total_customers = Customer.objects.count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_customers_last_30_days = Customer.objects.filter(created_at__gte=thirty_days_ago).count()

    stock_total_items_result = Product.objects.aggregate(total_items=Sum('stock_quantity'))
    stock_total_items = stock_total_items_result['total_items'] or 0

    total_revenue_result = FinancialRecord.objects.filter(status='PAGO').aggregate(total=Sum('sale__total_value'))
    total_revenue = total_revenue_result['total'] or 0
    total_expenses = 0 # Placeholder, pode ser implementado depois

    current_month = timezone.now().month
    current_year = timezone.now().year
    
    monthly_entries_result = StockMovement.objects.filter(
        movement_type='ENTRADA', 
        timestamp__year=current_year,
        timestamp__month=current_month
    ).aggregate(total=Sum('quantity'))
    monthly_entries = monthly_entries_result['total'] or 0

    monthly_exits_result = StockMovement.objects.filter(
        movement_type='SAIDA',
        timestamp__year=current_year,
        timestamp__month=current_month
    ).aggregate(total=Sum('quantity'))
    monthly_exits = monthly_exits_result['total'] or 0

    # ================================================================
    # ========= 2. NOVA LÓGICA PARA ALERTA DE ESTOQUE BAIXO =========
    # ================================================================
    low_stock_products = Product.objects.filter(
        minimum_stock__gt=0,  # Apenas produtos onde o estoque mínimo foi definido
        stock_quantity__lte=F('minimum_stock') # Compara o estoque atual com o mínimo
    )

    context = {
        'total_customers': total_customers,
        'new_customers': new_customers_last_30_days,
        'stock_total_items': stock_total_items,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'monthly_entries': monthly_entries,
        'monthly_exits': monthly_exits,
        # 3. Adicionamos a lista de produtos ao contexto
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/dashboard.html', context)

# FUNÇÃO DE PESQUISA (sem alterações)
@login_required
def search_results_view(request):
    query = request.GET.get('q', '')
    product_results = []
    
    if query:
        product_results = Product.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        )

    context = {
        'query': query,
        'product_results': product_results,
    }
    return render(request, 'dashboard/search_results.html', context)