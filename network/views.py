import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User,Post


def index(request):
    if request.method == "POST":
        user= request.user
        content=request.POST['newPost']

        Post.objects.create_Post(user,content)

        return render(request, "network/index.html",{
            "message": "Post Created",
            "posts": Post.objects.filter(user=user)
        })

    else:
        return render(request, "network/index.html")


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


def allPosts(request):
    return render(request, "network/allPosts.html",{
        "Posts": Post.objects.all().order_by('-timeStamp')
    })

def following(request):
    followingSet = request.user.following.all()
    postSet=Post.objects.none()

    for usr in followingSet:
        postSet=postSet | (Post.objects.filter(user=usr.id))

    return render(request, "network/following.html",{
        "Posts": postSet.order_by('-timeStamp')
    })

def profilePage(request,userid):
    return render(request, "network/profilePage.html",{
        "Posts": Post.objects.filter(user=userid),
        "User": User.objects.get(id=userid),
        "Following": User.objects.get(id=userid).following.all().distinct().count(),
        "Followers": User.objects.get(id=userid).followers.all().distinct().count()
        
    })

def follow(request,userid):
    user = request.user
    target = User.objects.get(id=userid)
    user.following.add(target)
    target.followers.add(user)
    user.save()
    target.save()
    return HttpResponseRedirect(reverse("allPosts"))

def unfollow(request,userid):
    user = request.user
    target = User.objects.get(id=userid)
    user.following.remove(target)
    target.followers.remove(user)
    user.save()
    target.save()
    return HttpResponseRedirect(reverse("allPosts"))

def savePost(request,number):
    
    if request.method == "PUT":
        data = json.loads(request.body)
        user = User.objects.get(username=request.user.username)
        posts=Post.objects.filter(user=user.id)
        specificPost = posts[number-1]
        specificPost.content = data["content"]
        specificPost.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
    
def like(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(content = data["content"])
        post.like = post.like + 1
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)