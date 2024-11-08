from django.contrib import admin

# Register your models here.
from .models import *
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'message', 'date')  # Add 'date' here
admin.site.register(Room)
admin.site.register(Message)