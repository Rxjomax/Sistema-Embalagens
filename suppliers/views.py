# Ficheiro: suppliers/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q # Importamos o Q para a busca

from .models import Supplier
from .forms import SupplierForm

class SupplierListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'

    def test_func(self):
        return self.request.user.has_perm('suppliers.view_supplier')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            # Filtra por nome fantasia, razão social, ou CNPJ/CPF
            queryset = queryset.filter(
                Q(trade_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(doc_number__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class SupplierCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    def test_func(self):
        return self.request.user.has_perm('suppliers.add_supplier')

class SupplierUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    def test_func(self):
        return self.request.user.has_perm('suppliers.change_supplier')

class SupplierDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers:supplier_list')
    def test_func(self):
        return self.request.user.has_perm('suppliers.delete_supplier')