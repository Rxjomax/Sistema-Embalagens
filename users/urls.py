from django.urls import path
from .views import (
    UserListView,
    user_create_view, # Usando a view baseada em função
    user_update_view, # Usando a view baseada em função
    UserDeleteView,
    UserPermissionsView # Importamos a nova view
)

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('adicionar/', user_create_view, name='user_add'),
    path('<int:pk>/editar/', user_update_view, name='user_update'),
    path('<int:pk>/excluir/', UserDeleteView.as_view(), name='user_delete'),
    
    # NOVA ROTA PARA A PÁGINA DE PERMISSÕES
    path('<int:user_id>/permissoes/', UserPermissionsView.as_view(), name='user_permissions'),
]