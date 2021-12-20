from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,  HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms
# from django.forms import ModelForm
from django.utils import timezone

from .models import User, Post, Like, Followers

class NewPostForm(forms.Form):
    title = forms.CharField(label="title")
    body = forms.CharField(label="body")


def index(request):
    return render(request, "network/index.html", {
        "posts": reversed(Post.objects.all()),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def add_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data["title"]
            post.body = form.cleaned_data["body"]
            post.user = User.objects.get(username = request.user.username)
            post.timestamp = timezone.now

            post.save()

            return HttpResponseRedirect(reverse("index"))
        
        else:
            return HttpResponse(form.errors)
        
    else:
        form = NewPostForm()

        return HttpResponseRedirect(reverse("index"))
