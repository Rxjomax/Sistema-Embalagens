# Ficheiro: dashboard/context_processors.py

from .models import Notification
from users.models import Profile  # 1. Importamos o modelo de Perfil

def notifications_context(request):
    context = {}
    if request.user.is_authenticated:
        # Lógica de notificações (existente)
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        context['notifications'] = unread_notifications
        context['notification_count'] = unread_notifications.count()
        
        # --- 2. NOVA LÓGICA PARA BUSCAR O PERFIL DO USUÁRIO ---
        # Usamos um try/except para o caso de um usuário ainda não ter um perfil criado
        try:
            # Assumindo que o related_name no seu modelo User para Profile é 'profile'
            profile = request.user.profile
            context['user_profile'] = profile
        except Profile.DoesNotExist:
            context['user_profile'] = None

    return context