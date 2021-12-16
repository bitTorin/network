from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.title}"

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='like_user')
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return f"{self.user}: {self.posts}"

class Followers(models.Model):
    account = models.ForeignKey('User', on_delete=models.CASCADE, related_name='account')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return f"{self.account}: {self.follower}"