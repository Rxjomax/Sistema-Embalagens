from django.urls import path
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView
)

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('adicionar/', CategoryCreateView.as_view(), name='category_add'),
    path('<int:pk>/editar/', CategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/excluir/', CategoryDeleteView.as_view(), name='category_delete'),
]
