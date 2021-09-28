from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreation, CustomUserChange

CustomUser = get_user_model()

class CustomAdmin(UserAdmin):
    add_form = CustomUserCreation
    form = CustomUserChange
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomAdmin)
