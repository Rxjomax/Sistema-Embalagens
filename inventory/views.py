# Ficheiro: inventory/views.py

from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q

from products.models import Product
from .forms import StockMovementForm
from .models import StockMovement

class InventoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def test_func(self):
        # Permite o acesso se o usuário for superuser ou tiver a permissão para ver movimentos de estoque
        return self.request.user.is_superuser or self.request.user.has_perm('inventory.view_stockmovement')

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(code__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

@login_required
@permission_required('inventory.add_stockmovement', raise_exception=True)
def create_stock_movement(request, movement_type):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.user = request.user
            movement.movement_type = movement_type.upper()
            movement.save()
            messages.success(request, f"Movimento de {movement_type.lower()} registado com sucesso.")
            return redirect('inventory:inventory_list')
    else:
        form = StockMovementForm()

    context = {
        'form': form,
        'movement_type': movement_type.capitalize()
    }
    return render(request, 'inventory/stock_movement_form.html', context)