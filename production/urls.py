# Ficheiro: production/urls.py (VERSÃO CORRIGIDA)

from django.urls import path
from .views import (
    # 1. Corrigimos a importação: trocamos 'KanbanBoardView' por 'kanban_board_view'
    kanban_board_view,
    ProductionStageCreateView,
    ProductionStageUpdateView,
    ProductionStageDeleteView,
    ProductionOrderCreateView,
    ProductionOrderUpdateView,
    ProductionOrderDeleteView,
    production_order_details,
    update_order_stage
)

app_name = 'production'

urlpatterns = [
    # 2. Corrigimos a rota: chamamos a função diretamente, sem '.as_view()'
    path('', kanban_board_view, name='kanban_board'),
    
    # O restante das URLs já estava correto
    path('estagio/adicionar/', ProductionStageCreateView.as_view(), name='stage_add'),
    path('estagio/<int:pk>/editar/', ProductionStageUpdateView.as_view(), name='stage_update'),
    path('estagio/<int:pk>/excluir/', ProductionStageDeleteView.as_view(), name='stage_delete'),
    
    path('ordem/adicionar/', ProductionOrderCreateView.as_view(), name='order_add'),
    path('ordem/<int:pk>/editar/', ProductionOrderUpdateView.as_view(), name='order_update'),
    path('ordem/<int:pk>/excluir/', ProductionOrderDeleteView.as_view(), name='order_delete'),
    
    # URLs da API
    path('api/ordem/<int:pk>/detalhes/', production_order_details, name='api_order_details'),
    path('api/update_order_stage/', update_order_stage, name='api_update_order_stage'),
]