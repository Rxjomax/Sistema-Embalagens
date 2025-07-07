# Ficheiro: sales/views.py (VERSÃO CORRIGIDA E FINAL)

from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import json
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Sale
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
    success_url = reverse_lazy('sales:sale_list')

    def test_func(self):
        return self.request.user.has_perm('sales.add_sale')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        product_prices = {str(p.id): str(p.unit_price) for p in products}
        context['product_prices_json'] = json.dumps(product_prices)
        
        # Garante que o formset seja passado corretamente, mesmo em caso de erro
        if 'item_formset' not in kwargs:
            if self.request.POST:
                context['item_formset'] = SaleItemFormSet(self.request.POST, prefix='items')
            else:
                context['item_formset'] = SaleItemFormSet(prefix='items')
        else:
            context['item_formset'] = kwargs['item_formset']
            
        return context

    def post(self, request, *args, **kwargs):
        # self.object não existe em CreateView antes do form_valid
        form = self.get_form()
        item_formset = SaleItemFormSet(request.POST, prefix='items')

        if form.is_valid() and item_formset.is_valid():
            return self.form_valid(form, item_formset)
        else:
            # Se houver erros, chama o form_invalid com ambos os formulários
            return self.form_invalid(form, item_formset)

    def form_valid(self, form, item_formset):
        with transaction.atomic():
            form.instance.seller = self.request.user
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()

            total = sum(item.total for item in self.object.items.all() if item.total is not None)
            self.object.total_value = total
            self.object.save()

            try:
                first_stage = ProductionStage.objects.order_by('order').first()
                if not first_stage:
                    raise Exception("Nenhum estágio de produção foi encontrado.")
                
                for item in self.object.items.all():
                    ProductionOrder.objects.create(
                        order_number=f"OP-{self.object.pk}-{item.pk}", product=item.product,
                        quantity=item.quantity, stage=first_stage, customer=self.object.customer,
                        created_by=self.object.seller, sale=self.object)
                    StockMovement.objects.create(
                        product=item.product, quantity=item.quantity, movement_type='SAIDA',
                        user=self.object.seller, notes=f"Saída referente à Venda #{self.object.pk}")
                
                messages.success(self.request, "Venda registrada e Ordem de Produção enviada para o Kanban!")
            
            except Exception as e:
                messages.error(self.request, f"Venda registrada, mas ocorreu um erro ao gerar a Ordem de Produção: {e}")
        
        return redirect(self.get_success_url())

    def form_invalid(self, form, item_formset=None):
        messages.error(self.request, "Por favor, corrija os erros abaixo.")
        return self.render_to_response(self.get_context_data(form=form, item_formset=item_formset))

def customer_search_view(request):
    query = request.GET.get('term', '')
    customers = Customer.objects.filter(name__icontains=query)[:10]
    results = [{'id': c.id, 'text': c.name} for c in customers]
    return JsonResponse(results, safe=False)