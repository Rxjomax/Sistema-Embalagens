# Ficheiro: products/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
import pandas as pd
from django.db.models import Q

from .models import Product
from categories.models import Category
from .forms import ProductForm

class ProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('products.view_product')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(code__icontains=query)
            )
        # --- ORDENAÇÃO ADICIONADA AQUI ---
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('products.add_product')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('products.change_product')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('products.delete_product')

@permission_required('products.add_product', raise_exception=True)
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