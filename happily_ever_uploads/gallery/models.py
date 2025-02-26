from django.db import models
from django.contrib.auth import get_user_model

class Image(models.Model):
    name = models.CharField(max_length=255)  
    image = models.ImageField(upload_to='guestbook/')  
    comment = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='owned_Image'
   )

    def __str__(self):
        return f"Image by {self.name}"
