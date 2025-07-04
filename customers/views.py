# Ficheiro: customers/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd

from .models import Customer
from .forms import CustomerForm

class CustomerListView(LoginRequiredMixin, ListView):
    # ... (sem alterações aqui)
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    # ... (sem alterações aqui)
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer_list')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    # ... (sem alterações aqui)
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer_list')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    # ... (sem alterações aqui)
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:customer_list')

def import_customers_view(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        # ... (código de verificação do arquivo) ...

        try:
            df = pd.read_excel(excel_file).astype(str) # Lê tudo como texto
            df.columns = [str(col).lower().strip().replace(' ', '_') for col in df.columns]

            for index, row in df.iterrows():
                # AGORA VERIFICA PELO TELEFONE
                if pd.isna(row.get('telefone')):
                    continue
                
                # Prepara os dados para salvar
                customer_data = {
                    'name': row.get('nome'),
                    'cep': row.get('cep'),
                    'address': row.get('logradouro'),
                    'number': row.get('numero'),
                    'city': row.get('cidade'),
                    'state': row.get('uf'),
                    'company_name': row.get('razao_social', ''),
                    'doc_number': row.get('cpf_cnpj', ''),
                    'email': row.get('email', ''),
                }
                
                # Limpa chaves vazias
                customer_data = {k: v for k, v in customer_data.items() if pd.notna(v)}
                
                # USA O TELEFONE COMO CHAVE
                phone_number = str(row['telefone']).strip()
                Customer.objects.update_or_create(
                    phone=phone_number,
                    defaults=customer_data
                )

            messages.success(request, "Planilha de clientes processada com sucesso!")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")

        return redirect('customers:customer_list')
    
    return render(request, 'customers/customer_import.html')