from django.db import models

from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=255)  
    image = models.ImageField(upload_to='guestbook/')  
    comment = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image by {self.name}"
