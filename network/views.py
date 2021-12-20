from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,  HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.core.paginator import Paginator

from .models import User, Post, Like, Followers

class NewPostForm(forms.Form):
    new_post_title = forms.CharField(label="new_post_title")
    new_post_body = forms.CharField(label="new_post_body")


def index(request):
    posts = Post.objects.order_by('-timestamp')
    paginator = Paginator(posts, 10) # Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'page_obj': page_obj
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
            post.title = form.cleaned_data['new_post_title']
            post.body = form.cleaned_data['new_post_body']
            post.user = User.objects.get(username = request.user.username)
            post.timestamp = timezone.now

            post.save()

            return HttpResponseRedirect(reverse("index"))
        
        else:
            return HttpResponse("Invalid request, please try again")
        
    else:
        form = NewPostForm()

    return HttpResponseRedirect(reverse("index"))

def profile(request, user_name):
    user = User.objects.get(username = user_name)
    return render(request, "network/profile.html", {
        "user": user,
        "posts": reversed(Post.objects.filter(user = user)),
    })

@login_required
def following(request, user):
    user = User.objects.get(username = user)
    return render(request, "network/profile.html", {
        "posts": reversed(Post.user.objects.filter(user = user)),
    })