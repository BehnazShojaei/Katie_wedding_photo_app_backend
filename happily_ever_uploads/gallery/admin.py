from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'uploaded_by', 'uploaded_at', 'get_image_url')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('caption', 'uploaded_by__username')
    readonly_fields = ('uploaded_at', 'get_image_url')

    def get_image_url(self, obj):
        return obj.image.url if obj.image else ''
    get_image_url.short_description = 'Image URL'

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
