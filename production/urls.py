# Ficheiro: production/urls.py

from django.urls import path
from .views import (
    kanban_board_view,
    ProductionStageCreateView,
    ProductionStageUpdateView,
    ProductionStageDeleteView,
    ProductionOrderUpdateView,
    ProductionOrderDeleteView,
    production_order_details,
    update_order_stage
)

app_name = 'production'

urlpatterns = [
    # Rotas do Kanban
    path('', kanban_board_view, name='kanban_board'),
    path('api/ordem/<int:pk>/detalhes/', production_order_details, name='api_order_details'),
    path('api/update-stage/', update_order_stage, name='api_update_order_stage'),

    # Rotas para gerenciar Estágios
    path('estagios/adicionar/', ProductionStageCreateView.as_view(), name='stage_add'),
    path('estagios/<int:pk>/editar/', ProductionStageUpdateView.as_view(), name='stage_update'),
    path('estagios/<int:pk>/excluir/', ProductionStageDeleteView.as_view(), name='stage_delete'),

    # Rotas para gerenciar Ordens (sem a de criar)
    path('ordem/<int:pk>/editar/', ProductionOrderUpdateView.as_view(), name='order_update'),
    path('ordem/<int:pk>/excluir/', ProductionOrderDeleteView.as_view(), name='order_delete'),
]