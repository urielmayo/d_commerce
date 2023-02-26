from apps.notifications.models import Notification

class NotificationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            notifications = Notification.objects.filter(
                receiver=self.request.user.profile,
                is_read=False
            ).order_by('-created_at')[:3]
            context['unread_notifications'] = notifications
        return context
