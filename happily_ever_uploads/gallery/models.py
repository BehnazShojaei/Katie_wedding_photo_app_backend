from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class Image(models.Model):
    image = models.ImageField(upload_to='media/', storage=S3Boto3Storage())
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_images'
    )

    def __str__(self):
        return f"Image uploaded by {self.uploaded_by} at {self.uploaded_at}"
