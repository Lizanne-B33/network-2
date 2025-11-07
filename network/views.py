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
    memberName = ""
    # Authenticated users view their their Posts and can enter a new post
    if request.user.is_authenticated:
        memberName = request.user.username
        return render(request, "network/index.html", {'form': form, 'memberName': memberName})
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
    username = ""
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

# ---------------------------------------------------------------
# A logged in user (member of the Social Network) can
# Add new posts, # Edit their own posts, and like anyone's posts.
# ---------------------------------------------------------------


@csrf_exempt
@login_required
def add_post(request):
    # Add Post: Sets up the Form Model for a new post
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

# Edit Post: uses an Edit Button that is only displayed if the
# Member is viewing their own post.  This edit button enables
# the member to modify and save their own post.

# EDIT TODO

# Like toggle: any logged in user can like or unlike a post
# LIKE TODO


def check_like_status(request, id):
    post = Post.objects.get(id=id)
    liked = request.user in post.member_likes.all()
    return JsonResponse({'liked': liked})


def update_likes(request, id):
    print('update has been called')
    post = get_object_or_404(Post, id=id)
    print('Post ID' + str(id))
    print('user ID' + str(request.user))
    post.member_likes.add(request.user)
    post.save()
    post.like()
    count_likes(id)
    return HttpResponseRedirect(reverse('index'))


def update_unlikes(request, id):
    post = get_object_or_404(Post, id=id)
    post.member_likes.remove(request.user)
    post.save()
    post.unlike()
    count_likes(id)
    return HttpResponseRedirect(reverse('index'))


def count_likes(request, id):
    post = get_object_or_404(Post, id=id)
    count = post.member_likes
    return JsonResponse({'count': count})


# ---------------------------------------------------------------
# Any user (logged in or not) can view all posts
# Must be in chronological order.  Most recent first.
# I added a grouping by author.
# I intentionally added only the title to be displayed on the list
# I added a nice view of the full post that mimics a social media post.
# This view is accessed when the user clicks on the post title.
# ---------------------------------------------------------------
def feed(request):
    posts = Post.objects
    posts = posts.order_by("created_by", "-create_date").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


# ---------------------------------------------------------------
# Any user (logged in or not) can view the member's profile
# This is activated by clicking on the member's name from the list in all posts.
# The profile displays the number of followers, and followed by users.
# All of the user's posts are displayed in reverse chronological order.
# ---------------------------------------------------------------
def single_profile(request, id):
    # Creates the profile that the user sees when clicking on a user name.
    # Query for requested User
    try:
        member = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)

    # Return User contents
    if request.method == "GET":
        return JsonResponse(member.serialize())


def single_feed(request, created_by):
    # collects the data for the posts that were created by that user.
    # since created by is a FK, I need to look up the User object by user name then filter by the user.
    user = get_object_or_404(User, username=created_by)
    posts = Post.objects.filter(created_by=user)
    if posts:
        posts = posts.order_by("create_date").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)
    else:
        return JsonResponse({"text": "You don't have any posts yet."})


def single_post(request, id):
    # Query for requested Post
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return Post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())


def profiles(request):
    # Pulls all users.
    members = User.objects
    members = User.order_by("username").all()
    return JsonResponse([User.serialize() for member in members], safe=False)
# ---------------------------------------------------------------
# Logged in users (members) can choose to follow another member.
# This will give the members a page/view where they can see a
# list of posts limited to only the members that they follow.
# A member can not follow themselves.
# ---------------------------------------------------------------
# FOLLOW - TODO

# ---------------------------------------------------------------
# Pagination:
# Pagination should be deployed on any page displaying posts.
# Limit is set to 10 posts with next/previous buttons when
# the number of posts is greater than 10.
# ---------------------------------------------------------------
# Pagination - TODO
