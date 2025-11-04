import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Post
from .forms import (PostForm)

# ---------------------------------------------
# User Login/Logout Functions
# ---------------------------------------------


def index(request):
    form = PostForm()
    # Authenticated users view their their Posts and can enter a new post
    if request.user.is_authenticated:
        return render(request, "network/post_feed.html", {'form': form})
    # Everyone else can see the existing posts, and invited to register/sign in.
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
# ---------------------------------------------
# Post Functions
# ---------------------------------------------


@csrf_exempt
@login_required
def add_post(request):
    if request.method == 'POST':
        # Bind user input to the form
        form = PostForm(request.POST)
        # Server-side Validation
        print(request.FILES)
        if form.is_valid():
            my_title = form.cleaned_data['title']
            my_body = form.cleaned_data['body']
            # create the post object
            new_post = Post(title=my_title,
                            body=my_body,
                            created_by=request.user,
                            likes=0)
            new_post.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PostForm()
        print(form)
    return render(request, "network/index.html", {'form': form})


def feed(request):
    posts = Post.objects
    posts = posts.order_by("created_by", "-create_date").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

# since created by is a FK, I need to look up the User object by user name then filter by the user.


def single_feed(request, created_by):
    user = get_object_or_404(User, username=created_by)
    posts = Post.objects.filter(created_by=user)
    posts = posts.order_by("create_date").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def profiles(request):
    members = User.objects
    members = User.order_by("username").all()
    return JsonResponse([User.serialize() for member in members], safe=False)


def single_profile(request, id):
    # Query for requested User
    try:
        member = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)

    # Return User contents
    if request.method == "GET":
        return JsonResponse(member.serialize())


def single_post(request, id):
    # Query for requested Post
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return Post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
