from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

import datetime


def index(request):
    return render(request, "network/index.html",{
        "posts": Post.objects.all(),
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

def newPost(request):
    if request.method =="POST":
        postBody = request.POST["newPost_body"]
        username = request.user.username
        likes = 0
        newPostObj = Post(
            author=username,
            body=postBody,
            likes=likes)
        newPostObj.save()
        return render(request, "network/test.html", {
            "object": newPostObj,
        })

def profile(request, user_name):
    if(False):
        return render(request, "network/error.html",{
            "error": "user does not exist",
        })
    else:
        user = User.objects.get(username=user_name)
        posts = Post.objects.filter(author=user)
    return render(request, "network/profile.html",{
        "user":user,
        "posts":posts,
    })


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
