from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {
            'notifications': unread_notifications,
            'notification_count': unread_notifications.count(),
        }
    return {}
