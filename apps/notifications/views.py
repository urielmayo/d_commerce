from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from apps.notifications.models import Notification
# Create your views here.
@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    return redirect(notification.url)