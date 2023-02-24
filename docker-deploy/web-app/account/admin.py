from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from .forms import CustomUserCreationForm
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    
    model = MyUser
    list_display = ["email", "username",]

admin.site.register(MyUser, UserAdmin)