from django.contrib import admin
from .models import CustomUser,UserProfile
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display=['email','first_name','last_name','is_staff','is_active','date_joined']
    search_fields=['email','first_name','last_name']
    ordering=['email']
admin.site.register(CustomUser,CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user','first_name','last_name','created_at']
    search_fields=['user__email','first_name','last_name']
    ordering=['user__email']
admin.site.register(UserProfile,UserProfileAdmin)