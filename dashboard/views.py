# Ficheiro: dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Q, F
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.core.exceptions import PermissionDenied # 1. Importamos a exceção necessária

# Importamos os modelos de que precisamos
from customers.models import Customer
from products.models import Product
from finance.models import FinancialRecord
from inventory.models import StockMovement

@login_required
def dashboard_view(request):
    # =============================================
    # ========= VERIFICAÇÃO DE PERMISSÃO ADICIONADA =========
    # =============================================
    # Se o usuário logado pertence ao grupo "Vendedor", nega o acesso.
    if request.user.groups.filter(name='Vendedor').exists():
        raise PermissionDenied

    today = timezone.now()
    current_year = today.year
    current_month = today.month

    # --- Cálculos para os Cards de Resumo ---
    total_customers = Customer.objects.count()
    thirty_days_ago = today - timedelta(days=30)
    new_customers_last_30_days = Customer.objects.filter(created_at__gte=thirty_days_ago).count()
    
    total_revenue_result = FinancialRecord.objects.filter(
        status='PAGO', sale__sale_date__year=current_year, sale__sale_date__month=current_month
    ).aggregate(total=Sum('sale__total_value'))
    total_revenue = total_revenue_result['total'] or Decimal('0.00')

    total_expenses_result = StockMovement.objects.filter(
        movement_type='ENTRADA', timestamp__year=current_year, timestamp__month=current_month
    ).aggregate(total=Sum('total_cost'))
    total_expenses = total_expenses_result['total'] or Decimal('0.00')
    
    profit = total_revenue - total_expenses
    low_stock_products = Product.objects.filter(minimum_stock__gt=0, stock_quantity__lte=F('minimum_stock'))

    # --- DADOS PARA O GRÁFICO DE FATURAMENTO MENSAL (LINHA) ---
    revenue_chart_labels = []
    revenue_chart_data = []
    for i in range(5, -1, -1):
        month_date = today - relativedelta(months=i)
        revenue_chart_labels.append(month_date.strftime('%b/%y').capitalize())
        
        monthly_revenue = FinancialRecord.objects.filter(
            status='PAGO', sale__sale_date__year=month_date.year, sale__sale_date__month=month_date.month
        ).aggregate(total=Sum('sale__total_value'))['total'] or 0
        revenue_chart_data.append(float(monthly_revenue))

    # --- DADOS PARA O GRÁFICO DE ESTOQUE (BARRAS) ---
    top_stock_products = Product.objects.order_by('-stock_quantity').filter(stock_quantity__gt=0)[:5]
    stock_chart_labels = [p.name for p in top_stock_products]
    stock_chart_data = [p.stock_quantity for p in top_stock_products]

    context = {
        'total_customers': total_customers,
        'new_customers': new_customers_last_30_days,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'profit': profit,
        'low_stock_products': low_stock_products,
        
        # Dados para o gráfico de receita
        'revenue_chart_labels': revenue_chart_labels,
        'revenue_chart_data': revenue_chart_data,
        'stock_chart_labels': stock_chart_labels,
        'stock_chart_data': stock_chart_data,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def search_results_view(request):
    query = request.GET.get('q', '')
    product_results = []
    if query:
        product_results = Product.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        )
    context = { 'query': query, 'product_results': product_results, }
    return render(request, 'dashboard/search_results.html', context)