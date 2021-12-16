from django.contrib import admin

from .models import User, Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "body")

admin.site.register(User)
admin.site.register(Post, PostAdmin)