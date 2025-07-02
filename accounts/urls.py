# accounts/urls.py
# --- CORRIGIDO ---

from django.urls import path
from .views import CustomLoginView, profile_view
from django.contrib.auth import views as auth_views

app_name = 'accounts' # <--- ADICIONE ESTA LINHA AQUI

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # É uma boa prática definir para onde o usuário vai depois do logout
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'), # <--- ALTERADO PARA USAR O NAMESPACE
    path('perfil/', profile_view, name='profile'),

    path('password_reset/', 
          auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), 
          name='password_reset'),
    path('password_reset/done/', 
          auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
          name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
          auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
          name='password_reset_confirm'),
    path('reset/done/', 
          auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
          name='password_reset_complete'),
]