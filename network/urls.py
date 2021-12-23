
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/<str:user_name>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("unfollow/<int:profile_id>", views.unfollow, name="unfollow"),
    path("like_post", views.like_post, name="like_post"),
    path("unlike_post", views.unlike_post, name="unlike_post"),
]
