# Ficheiro: production/views.py

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta

from .models import ProductionStage, ProductionOrder
from .forms import ProductionStageForm, ProductionOrderForm
from finance.models import FinancialRecord
from sales.models import Sale
from customers.models import Customer
from products.models import Product

@login_required
def kanban_board_view(request):
    stages = ProductionStage.objects.prefetch_related(
        'orders__product', 
        'orders__customer', 
        'orders__sale_item'
    ).all()
    
    last_stage = ProductionStage.objects.order_by('-order').first()
    delay_threshold = timezone.now() - timedelta(days=3)

    stages_list = []
    for stage in stages:
        orders_data = []
        for order in stage.orders.all():
            is_delayed = (order.created_at < delay_threshold) and (stage.id != last_stage.id if last_stage else True)
            order.is_delayed = is_delayed
            orders_data.append(order)

        stages_list.append({
            'id': stage.id,
            'name': stage.name,
            'pk': stage.pk,
            'orders_list': orders_data
        })

    all_customers = Customer.objects.order_by('name')
    all_products = Product.objects.order_by('name')

    context = {
        'stages': stages_list,
        'all_customers': all_customers,
        'all_products': all_products,
    }
    
    return render(request, 'production/kanban_board.html', context)

# --- VIEWS DE GESTÃO DE ESTÁGIOS E ORDENS ---
class ProductionStageCreateView(LoginRequiredMixin, CreateView):
    model = ProductionStage
    form_class = ProductionStageForm
    template_name = 'production/stage_form.html'
    success_url = reverse_lazy('production:kanban_board')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Adicionar Novo Estágio"
        return context

class ProductionStageUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductionStage
    form_class = ProductionStageForm
    template_name = 'production/stage_form.html'
    success_url = reverse_lazy('production:kanban_board')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Renomear Estágio: {self.object.name}"
        return context

class ProductionStageDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductionStage
    template_name = 'production/stage_confirm_delete.html'
    success_url = reverse_lazy('production:kanban_board')
    def form_valid(self, form):
        messages.success(self.request, f"O estágio '{self.object.name}' foi excluído.")
        return super().form_valid(form)

class ProductionOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductionOrder
    form_class = ProductionOrderForm
    template_name = 'production/order_form.html'
    success_url = reverse_lazy('production:kanban_board')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editando Ordem: {self.object.order_number}"
        return context

class ProductionOrderDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductionOrder
    template_name = 'production/order_confirm_delete.html'
    success_url = reverse_lazy('production:kanban_board')
    def form_valid(self, form):
        messages.success(self.request, f"A ordem '{self.object.order_number}' foi excluída.")
        return super().form_valid(form)

# --- APIs ---
@login_required
def production_order_details(request, pk):
    order = get_object_or_404(
        ProductionOrder.objects.select_related(
            'product', 'customer', 'stage', 'sale__seller', 'sale_item'
        ), pk=pk
    )
    
    gramatura_display = f"{order.sale_item.gramatura}g" if order.sale_item and order.sale_item.gramatura is not None else '-'
    
    data = {
        'order_number': order.order_number,
        'product_name': order.product.name,
        'quantity': order.quantity,
        'customer_name': order.customer.name if order.customer else 'N/A',
        'notes': order.notes or 'Nenhuma observação.',
        'sale_id': order.sale.pk if order.sale else None,
        'seller_name': order.sale.seller.username if order.sale and order.sale.seller else 'N/A',
        'created_at': order.created_at.isoformat(),
        'edit_url': reverse('production:order_update', kwargs={'pk': order.pk}),
        'delete_url': reverse('production:order_delete', kwargs={'pk': order.pk}),
        'sale_url': reverse('finance:record_manage', kwargs={'pk': order.sale.financial_record.pk}) if order.sale and hasattr(order.sale, 'financial_record') else '#',
        'cor_embalagem': order.sale_item.cor_embalagem if order.sale_item and order.sale_item.cor_embalagem else '-',
        'cor_logo_1': order.sale_item.cor_logo_1 if order.sale_item and order.sale_item.cor_logo_1 else '-',
        'cor_logo_2': order.sale_item.cor_logo_2 if order.sale_item and order.sale_item.cor_logo_2 else '-',
        'gramatura': gramatura_display,
        # --- DADOS DE ENDEREÇO ADICIONADOS AO JSON ---
        'address': f"{order.customer.address}, {order.customer.number}" if order.customer else '-',
        'city_state': f"{order.customer.city} - {order.customer.state}" if order.customer else '-',
        'cep': order.customer.cep if order.customer else '-',
    }
    return JsonResponse(data)

@login_required
@require_POST
def update_order_stage(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id'); new_stage_id = data.get('stage_id')
        order = get_object_or_404(ProductionOrder, pk=order_id); new_stage = get_object_or_404(ProductionStage, pk=new_stage_id)
        order.stage = new_stage; order.save()
        last_stage_order = ProductionStage.objects.aggregate(max_order=Max('order'))['max_order']
        if new_stage.order == last_stage_order and order.sale:
            FinancialRecord.objects.get_or_create(sale=order.sale, defaults={'status': 'AGUARDANDO'})
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)