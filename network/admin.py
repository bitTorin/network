from django.contrib import admin

from .models import User, Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp", "title", "body")

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("liked_posts",)

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)