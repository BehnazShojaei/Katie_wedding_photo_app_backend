from django.contrib.auth.models import AbstractUser
from django.db import models

class PasscodeGroup(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"

class CustomUser(AbstractUser):
    is_guest = models.BooleanField(default=False)
    passcode_group = models.ForeignKey(PasscodeGroup, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
