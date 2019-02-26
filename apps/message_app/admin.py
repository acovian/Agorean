from django.contrib import admin

# Register your models here.
from .models import Message, Comment, Like

admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Like)
