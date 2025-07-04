# Ficheiro: products/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import pandas as pd
from django.db.models import Q

from .models import Product
from categories.models import Category
from .forms import ProductForm

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        print("--- Iniciando busca de produtos ---") # DEBUG
        queryset = super().get_queryset()
        print(f"Passo 1: Encontrados {queryset.count()} produtos no total.") # DEBUG
        
        # Usamos .strip() para remover espaços em branco no início e no fim
        query = self.request.GET.get('q', '').strip()
        print(f"Passo 2: Termo de busca recebido: '{query}'") # DEBUG

        # A verificação 'if query:' agora é segura, pois uma string vazia após .strip() se torna False
        if query:
            print(f"Passo 3: Filtrando por '{query}'...") # DEBUG
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(code__icontains=query)
            )
            print(f"Passo 4: Encontrados {queryset.count()} produtos após o filtro.") # DEBUG
        else:
            print("Passo 3: Nenhum termo de busca válido, mostrando todos os produtos.") # DEBUG
        
        print("--- Finalizando busca ---") # DEBUG
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

# ... O resto do seu arquivo (CreateView, UpdateView, etc.) continua igual ...
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

def import_products_view(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        if not excel_file or not excel_file.name.endswith('.xlsx'):
            messages.error(request, "Formato de ficheiro inválido. Por favor, envie um ficheiro .xlsx")
            return redirect('products:product_import')
        try:
            df = pd.read_excel(excel_file)
            df.columns = [str(col).lower().replace(' ', '').replace('ç', 'c').replace('ã', 'a') for col in df.columns]
            for index, row in df.iterrows():
                if pd.isna(row.get('codigo')) or pd.isna(row.get('nome')):
                    continue
                try:
                    category = None
                    if pd.notna(row.get('categoria')):
                        category_name = str(row['categoria']).strip()
                        category_code = category_name.lower().replace(' ', '-')
                        category, created = Category.objects.get_or_create(name=category_name, defaults={'code': category_code})
                        if created:
                            messages.info(request, f"Nova categoria '{category_name}' foi criada automaticamente.")
                    unit_price = float(str(row.get('valorunitario', 0)).replace(',', '.'))
                    medida_x = float(str(row.get('medidax', 0)).replace(',', '.')) if pd.notna(row.get('medidax')) else None
                    medida_y = float(str(row.get('mediday', 0)).replace(',', '.')) if pd.notna(row.get('mediday')) else None
                    Product.objects.update_or_create(
                        code=str(row['codigo']).strip(),
                        defaults={ 'name': str(row['nome']).strip(), 'category': category, 'unit_price': unit_price, 'medida_x': medida_x, 'medida_y': medida_y, }
                    )
                except Exception as e:
                    messages.error(request, f"Erro ao processar a linha {index + 2}: {e}")
                    continue
            messages.success(request, "Planilha de produtos processada com sucesso!")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return redirect('products:product_list')
    return render(request, 'products/product_import.html')