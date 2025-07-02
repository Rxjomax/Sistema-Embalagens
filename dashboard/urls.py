# dashboard/urls.py
# --- CORRIGIDO ---

from django.urls import path
from .views import dashboard_view, search_results_view # Importa suas views de verdade

app_name = 'dashboard' # <--- ESTÁ CORRETO AQUI

urlpatterns = [
    # Renomeei para 'main' para ser mais claro que é a rota principal do dashboard
    path('', dashboard_view, name='main'), # <--- ALTERADO O NOME DA ROTA
    path('pesquisa/', search_results_view, name='search_results'),
]