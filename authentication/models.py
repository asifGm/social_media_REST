from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6, editable=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {'verified' if self.is_verified else 'pending'}"


    def save(self, *args, **kwargs):

        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)

        return super().save(*args, **kwargs)