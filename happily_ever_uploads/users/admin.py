from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'username', 'email', 'is_superuser', 'is_guest']  
    list_filter = ['is_superuser', 'is_staff', 'is_guest']  

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_guest',)}),  
    )

admin.site.register(CustomUser, CustomUserAdmin)
