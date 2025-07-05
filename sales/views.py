from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import json
from .models import Sale
from .forms import SaleForm, SaleItemFormSet
from products.models import Product
from production.models import ProductionOrder, ProductionStage
from inventory.models import StockMovement

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
        # ... (resto do seu código do get_context_data)
        products = Product.objects.all()
        product_prices = {str(p.id): str(p.unit_price) for p in products}
        context['product_prices_json'] = json.dumps(product_prices)
        if self.request.POST:
            context['item_formset'] = SaleItemFormSet(self.request.POST, prefix='items')
        else:
            context['item_formset'] = SaleItemFormSet(prefix='items')
        return context

    def form_valid(self, form):
        # ... (resto do seu código do form_valid)
        context = self.get_context_data()
        item_formset = context['item_formset']
        if item_formset.is_valid():
            with transaction.atomic():
                form.instance.seller = self.request.user
                self.object = form.save()
                item_formset.instance = self.object
                item_formset.save()
                total = 0
                for item in self.object.items.all():
                    total += item.total
                self.object.total_value = total
                self.object.save()
                try:
                    first_stage = ProductionStage.objects.order_by('order').first()
                    if first_stage:
                        for item in self.object.items.all():
                            ProductionOrder.objects.create(
                                order_number=f"OP-{self.object.pk}-{item.pk}", product=item.product,
                                quantity=item.quantity, stage=first_stage, customer=self.object.customer,
                                created_by=self.object.seller, sale=self.object)
                            StockMovement.objects.create(
                                product=item.product, quantity=item.quantity, movement_type='SAIDA',
                                user=self.object.seller, notes=f"Saída referente à Venda #{self.object.pk}")
                        messages.success(self.request, "Venda registrada e ordem de produção enviada com sucesso!")
                    else:
                        messages.warning(self.request, "Venda registrada, mas a ordem de produção FALHOU.")
                except Exception as e:
                    messages.error(self.request, f"Ocorreu um erro inesperado: {e}")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)