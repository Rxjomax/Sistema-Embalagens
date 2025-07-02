# core/urls.py
# --- CORRIGIDO ---

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # AGORA APONTA PARA 'accounts:login'
    path('', RedirectView.as_view(pattern_name='accounts:login', permanent=False)), # <--- CORRIGIDO
    
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('produtos/', include('products.urls', namespace='products')),
    path('categorias/', include('categories.urls', namespace='categories')),
    path('fornecedores/', include('suppliers.urls', namespace='suppliers')),
    path('clientes/', include('customers.urls', namespace='customers')),
    path('usuarios/', include('users.urls', namespace='users')),
    path('producao/', include('production.urls', namespace='production')),
    path('estoque/', include('inventory.urls', namespace='inventory')),
    path('vendas/', include('sales.urls', namespace='sales')),
    path('financeiro/', include('finance.urls', namespace='finance')),
    
    # Esta linha estava duplicada e foi REMOVIDA.
    # path('vendas/', include('sales.urls', namespace='sales')), 
]

# Linha para servir ficheiros de média em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)