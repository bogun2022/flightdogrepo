from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = [
        "email",
        "username",
        "user_ip",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("user_ip",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("user_ip",)}),)

admin.site.register(CustomUser, CustomUserAdmin)
