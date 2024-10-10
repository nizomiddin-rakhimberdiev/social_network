from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/avatar.jpg')
    phone = models.CharField(max_length=13, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message between {self.sender} and {self.receiver}'