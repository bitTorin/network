from django.contrib import admin

from .models import User, Post, Like, Followers

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp", "title", "body")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user")

class FollowerAdmin(admin.ModelAdmin):
    list_display = ("account", "follower")
    

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Followers, FollowerAdmin)