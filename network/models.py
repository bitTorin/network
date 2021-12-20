from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='post_user')

    def __str__(self):
        return f"{self.title}"

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user}: {self.post}"

class Followers(models.Model):
    account = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.account}: {self.follower}"