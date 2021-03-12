from django.contrib import admin
from .models import Setting, ContactMessage

# Register your models here.
admin.site.register(Setting)
admin.site.register(ContactMessage)
