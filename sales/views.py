# Ficheiro: sales/views.py

from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q

from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet
from products.models import Product
from production.models import ProductionOrder, ProductionStage
from inventory.models import StockMovement
from customers.models import Customer

class SaleListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'sales/sale_list.html'
    def test_func(self):
        return self.request.user.has_perm('sales.view_sale')

class SaleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('finance:record_list')

    def test_func(self):
        return self.request.user.has_perm('sales.add_sale')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'item_formset' not in kwargs:
            if self.request.POST:
                context['item_formset'] = SaleItemFormSet(self.request.POST, prefix='items')
            else:
                context['item_formset'] = SaleItemFormSet(prefix='items')
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        item_formset = SaleItemFormSet(request.POST, prefix='items')

        if form.is_valid() and item_formset.is_valid():
            return self.form_valid(form, item_formset)
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
            return self.render_to_response(
                self.get_context_data(form=form, item_formset=item_formset)
            )

    def form_valid(self, form, item_formset):
        try:
            with transaction.atomic():
                form.instance.seller = self.request.user
                self.object = form.save()
                
                # Salva os itens da venda, mas sem commit ainda
                items = item_formset.save(commit=False)
                for item in items:
                    item.sale = self.object
                    item.save() # Salva cada item individualmente
                
                # Agora que os itens têm um ID, podemos criar as ordens
                self.object.refresh_from_db()
                
                total = sum(item.get_total() for item in self.object.items.all() if item.product)
                self.object.total_value = total
                self.object.save()

                first_stage = ProductionStage.objects.order_by('order').first()
                if not first_stage:
                    raise Exception("Nenhum estágio de produção foi encontrado.")
                
                for item in self.object.items.all():
                    # ========================================================
                    # ========= CORREÇÃO APLICADA ABAIXO =========
                    # ========================================================
                    ProductionOrder.objects.create(
                        order_number=f"OP-{self.object.pk}-{item.pk}",
                        product=item.product,
                        quantity=item.quantity,
                        stage=first_stage,
                        customer=self.object.customer,
                        created_by=self.object.seller,
                        sale=self.object,
                        sale_item=item  # Conecta a Ordem de Produção ao Item da Venda
                    )
                    StockMovement.objects.create(
                        product=item.product, quantity=item.quantity, movement_type='SAIDA',
                        user=self.object.seller, notes=f"Saída referente à Venda #{self.object.pk}")
                
                messages.success(self.request, "Venda registrada e Ordem de Produção enviada para o Kanban!")
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro e a venda não foi salva: {e}")
            return self.render_to_response(self.get_context_data(form=form, item_formset=item_formset))
        
        return redirect(self.get_success_url())

def customer_search_view(request):
    query = request.GET.get('term', '')
    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )[:10]
    else:
        customers = Customer.objects.none()
    results = [{'id': c.id, 'text': f"{c.name} ({c.phone})"} for c in customers]
    return JsonResponse(results, safe=False)

def product_search_view(request):
    query = request.GET.get('term', '')
    if query:
        products = Product.objects.filter(
            Q(code__icontains=query) | Q(name__icontains=query)
        )[:10]
    else:
        products = Product.objects.none()
    results = [{'id': p.id, 'text': f"{p.name} ({p.code})", 'price': f"{p.unit_price:.2f}"} for p in products]
    return JsonResponse(results, safe=False)