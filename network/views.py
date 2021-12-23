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
import json
from itertools import chain


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
def post(request):
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
    profile = User.objects.get(username = user_name)
    posts = Post.objects.filter(user = profile).order_by('-timestamp')
    
    follower_list = profile.followers.all()
    followers = []
    for i in follower_list:
        f = i.follower
        followers.append(f)
    
    paginator = Paginator(posts, 10) # Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/profile.html', {
        "profile": profile,
        "followers": followers,
        "page_obj": page_obj
    })

@login_required
def following(request):
    active_user = User.objects.get(username = request.user)

     # Get all posts from users that current user follows
    posts = [users.get_followed_posts() for users in active_user.account.all()]

    # Chain posts together
    posts = list(chain(*posts))

    # Show 10 posts per page.
    paginator = Paginator(posts, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {
        "page_obj": page_obj
    })

@login_required
def follow(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        profile = data.get('profile')
        target = User.objects.get(username = profile)
        
        if user in target.followers.all():
            # Return negative response
            return HttpResponse("User already followed", status=404)

        else:
            
            # Save model instance of follow
            follow = Followers()
            follow.account = target
            follow.follower = user
            follow.save()

            # Return positive response
            return HttpResponse(status=201)

@login_required
def unfollow(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        profile = data.get('profile')
        target = User.objects.get(username = profile)
        unfollow_obj = Followers.objects.filter(account = target).filter(follower = user)
        
        if unfollow_obj.exists:
            
            # Delete model instance of follow
            unfollow_obj.delete()

            # Return positive response
            return HttpResponse(status=201)

        else:
            # Return negative response
            return HttpResponse("User already unfollowed", status=404)

@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        
        # Query for requested post - make sure
        post = Post.objects.get(pk=post_id, user=request.user)

        # Update post
        post.body = data.get('body')
        post.save()

        # Return positive response
        return HttpResponse(status=201)

@login_required
def like_post(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        post_id = data.get('post_id')
        liked_post = Post.objects.get(pk=post_id)
        
        # If user already liked post
        if user in liked_post.liked_by.all():

            # Return negative response
            return HttpResponse("Post already liked", status=404)
            
        # If not, like post
        else:
            liked_post.liked_by.add(user)

            # Return positive response
            return HttpResponse(status=201)

@login_required
def unlike_post(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        post_id = data.get('post_id')
        unliked_post = Post.objects.get(pk=post_id)

        # If user already unliked post
        if user not in unliked_post.liked_by.all():

            # Return negative response
            return HttpResponse("Post already unliked", status=404)

        # If not, unlike post
        else:
            unliked_post.liked_by.remove(user)

            # Return positive response
            return HttpResponse(status=201)

        

