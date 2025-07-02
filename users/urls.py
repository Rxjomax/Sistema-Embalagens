from django.urls import path
from .views import UserListView, user_create_view, user_update_view, UserDeleteView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('adicionar/', user_create_view, name='user_add'),
    path('<int:pk>/editar/', user_update_view, name='user_update'),
    path('<int:pk>/excluir/', UserDeleteView.as_view(), name='user_delete'),
]
