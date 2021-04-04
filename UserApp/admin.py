from django.contrib import admin
from .models import UserProfileModel
from django.contrib.auth.models import User
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','address','city','image_tag']
    list_filter = ['user',]

admin.site.register(UserProfileModel,UserProfileAdmin)
