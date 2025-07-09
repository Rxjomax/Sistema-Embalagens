# Ficheiro: customers/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from django.db.models import Q

from .models import Customer
from .forms import CustomerForm

class CustomerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 15

    def test_func(self):
        return self.request.user.has_perm('customers.view_customer')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(phone__icontains=query) | Q(doc_number__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class CustomerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer_list')
    
    def test_func(self):
        return self.request.user.has_perm('customers.add_customer')
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente cadastrado com sucesso!")
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer_list')
    
    def test_func(self):
        return self.request.user.has_perm('customers.change_customer')

    def form_valid(self, form):
        messages.success(self.request, "Cliente atualizado com sucesso!")
        return super().form_valid(form)

class CustomerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:customer_list')
    
    def test_func(self):
        return self.request.user.has_perm('customers.delete_customer')

    def form_valid(self, form):
        messages.success(self.request, "Cliente excluído com sucesso!")
        return super().form_valid(form)

@permission_required('customers.add_customer', raise_exception=True)
def import_customers_view(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        if not excel_file or not excel_file.name.endswith('.xlsx'):
            messages.error(request, "Formato de ficheiro inválido. Por favor, envie um ficheiro .xlsx")
            return redirect('customers:customer_import')
        try:
            df = pd.read_excel(excel_file).astype(str)
            df.columns = [str(col).lower().strip().replace(' ', '_') for col in df.columns]
            for index, row in df.iterrows():
                if pd.isna(row.get('telefone')):
                    continue
                customer_data = {
                    'name': row.get('nome'), 'cep': row.get('cep'), 'address': row.get('logradouro'),
                    'number': row.get('numero'), 'city': row.get('cidade'), 'state': row.get('uf'),
                    'company_name': row.get('razao_social', ''), 'doc_number': row.get('cpf_cnpj', ''),
                    'email': row.get('email', ''),
                }
                customer_data = {k: v for k, v in customer_data.items() if pd.notna(v)}
                phone_number = str(row['telefone']).strip()
                Customer.objects.update_or_create(phone=phone_number, defaults=customer_data)
            messages.success(request, "Planilha de clientes processada com sucesso!")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")
        return redirect('customers:customer_list')
    return render(request, 'customers/customer_import.html')