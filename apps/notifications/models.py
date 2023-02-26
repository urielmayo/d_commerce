from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from apps.users.models import Profile

class Notification(models.Model):
    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        null=True,
        blank=True
    )
    receiver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    @staticmethod
    def send_notification(sender, receiver, title, message, url):
        notification = Notification(
            sender=sender,
            receiver=receiver,
            title=title,
            message=message,
            url=url
        )
        notification.save()

    class Meta:
        ordering = ['-created_at']

# @receiver(post_save, sender=Notification)
# def mark_notification_as_read(sender, instance, **kwargs):
#     """
#     A signal receiver function to mark the notification as read when it is viewed.
#     """
#     if instance.is_read is False:
#         instance.is_read = True
#         instance.save()