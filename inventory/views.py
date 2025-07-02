from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .forms import StockMovementForm
from .models import StockMovement

class InventoryListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'products'
    paginate_by = 20

@login_required
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
