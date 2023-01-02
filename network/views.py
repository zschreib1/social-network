import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from operator import attrgetter
from datetime import datetime

# https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Post, FollowersCount, FollowingCount


def index(request):
    # Fetch the list of posts
    allposts = Post.objects.all().order_by('-posted_at')
    
    # Fetch the usernames who liked each post and store the data in a dict
    likesperpostid = {}
    keys_post_ids = []
    values_usernames = []
    
    for post in allposts:
        likes_for_posts = list(post.likes.all())
        print(likes_for_posts)
        post.id

        for user in likes_for_posts:
            print(f"{post.id}: {user.username}")
            #values.append(f"{post.id}: {user.username}")
            keys_post_ids.append(f"{post.id}")
            values_usernames.append(f"{user.username}")
    print(keys_post_ids)
    print(values_usernames)

    # create a dictionary from two lists without losing duplicate values
    # https://www.codegrepper.com/code-examples/typescript/create+a+dictionary+from+two+lists+without+losing+duplicate+values
    for key,value in zip(keys_post_ids,values_usernames):
        if key not in likesperpostid:
            likesperpostid[key]=[value]
        else:
            likesperpostid[key].append(value)

    currentpostid = key
    print("likesperpostid:", likesperpostid)
    print(likesperpostid[currentpostid])
    authenticateduser = user.username
    if authenticateduser in likesperpostid[currentpostid]:
        print(f"Post {currentpostid} liked by", authenticateduser)
    else:
        print(f"Post {currentpostid} not liked by", authenticateduser)

    # Pagination system
    page = request.GET.get('page', 1)
    paginator = Paginator(allposts, 10) # show 10 posts per page

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # authenticated user
    user = request.user

    if user.is_anonymous:
        # Pass the list to the context so as to be able to access it in the template
        context = {
            'allposts': allposts,
            'posts': posts,
            'user': user,
            'likesperpostid': likesperpostid
            #'likedposts': likedposts
        }
        print(context)

        return render(request, "network/index.html", context)
    
    else:

        # Pass the list to the context so as to be able to access it in the template
        context = {
            'allposts': allposts,
            'posts': posts,
            'user': user,
            'likesperpostid': likesperpostid
        }
        print(context)

        return render(request, "network/index.html", context)
        

    

@login_required
def newpost_view(request):
    # If the user submited the form to create a post
    if request.method == "POST":

        # The newpost is of tipe Post(object)
        newpost = Post()

        # Assign the data submitted via the newpost form to the object
        newpost.posted_by = request.user
        newpost.content = request.POST.get('content')
        # Save the object
        newpost.save()

        # Fetch the list of posts
        allposts = Post.objects.all().order_by('-posted_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(allposts, 10) # show 10 posts per page

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        # Authenticated user
        user = request.user

        # Pass the list to the context so as to be able to access it in the template
        context = {
            'allposts': allposts,
            'posts': posts,
            'user': user
        }

        return render(request, "network/index.html", context)
        
    
def profile_view(request, username):
    # Fetch information about the requested profile
    profile_username = username
    profile_user = User.objects.all().filter(username=profile_username)[0]

    # Fetch all posts for that user
    profile_posts = Post.objects.all().filter(posted_by=profile_user).order_by('-posted_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(profile_posts, 10) # show 10 posts per page

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Fetch follower count for that user
    followers = FollowersCount.objects.all().filter(profile=profile_user)
    followers_count = followers.count()
    print(followers)

    # authentified user
    user = request.user
    
    # Fetch following count for that profile_user
    following = FollowingCount.objects.all().filter(following=profile_user)
    print("accounts followed by: ", profile_user)
    #for obj in following:
    #    print(obj.profile.username)
    following_count = following.count()
    print(following_count)

    following_auth_user = FollowingCount.objects.all().filter(following=user)
    following_auth_user_count = following_auth_user.count()

    # Check if authenticated user already follows the profile
    if followers.filter(follower=user).exists():
        print("authenticated user already follows the profile")
        alreadyFollows = True # display unfollow button

        context = {
            'profile_username': profile_username,
            'profile_user': profile_user,
            'profile_posts': profile_posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'following_auth_user_count': following_auth_user_count,
            'alreadyFollows': alreadyFollows,
            'posts': posts,
            'user': user
        }

        return render(request, "network/profile.html", context)
 
    else: 
        alreadyFollows = False  # display follow button

        context = {
            'profile_username': profile_username,
            'profile_user': profile_user,
            'profile_posts': profile_posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'following_auth_user_count': following_auth_user_count,
            'alreadyFollows': alreadyFollows,
            'posts': posts,
            'user': user
        }

        return render(request, "network/profile.html", context)

@login_required
def follow_profile(request, username):
    # Fetch information about the requested profile
    profile_username = username
    profile_user = User.objects.all().filter(username=profile_username)[0]

    # Fetch all posts for that user
    profile_posts = Post.objects.all().filter(posted_by=profile_user).order_by('-posted_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(profile_posts, 10) # show 10 posts per page

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # authentified user
    user = request.user 

    alreadyFollows = True # Follow button displayed

    # Fetch followers for that user
    followers = FollowersCount.objects.all().filter(profile=profile_user)

    # Fetch following count for that profile_user
    following = FollowingCount.objects.all().filter(following=profile_user)
    print("accounts followed by: ", profile_user)

    # Fetch following count for auth user
    following_auth_user = FollowingCount.objects.all().filter(following=user)
    following_auth_user_count = following_auth_user.count()

    # If the user doesn't already follow the profile
    if followers.filter(follower=user).exists() == False:
        # Follow
        new_follower = FollowersCount()
        new_follower.profile = profile_user
        new_follower.follower = user.username
        new_follower.save()
        print("New follower: ", new_follower.follower)

        # TO DO : UPDATE FOLLOWING COUNT FOR THE AUTHENTICATED USER
        new_following = FollowingCount()
        new_following.profile = profile_user
        new_following.following = user.username
        print(new_following)
        new_following.save()
        
        # Refresh follower count for that user
        followers = FollowersCount.objects.all().filter(profile=profile_user)
        followers_count = followers.count()
        print(followers)

        # If user is authenticated, if user.username != profile_username
        # Refresh following count for that user
        following = FollowingCount.objects.all().filter(following=profile_user.username)
        following_count = following.count()
        print("accounts followed by: ", profile_user)
        print(following)
        print(following_count)

        # Refresh following count for auth user
        following_auth_user = FollowingCount.objects.all().filter(following=user)
        following_auth_user_count = following_auth_user.count()
        

        context = {
            'profile_username': profile_username,
            'profile_user': profile_user,
            'profile_posts': profile_posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'following_auth_user_count': following_auth_user_count,
            'alreadyFollows': alreadyFollows,
            'posts': posts,
            'user': user
            #'likedposts': likedposts
        }
    # Don't save the follower as user already follows the profile
    else: 
        # Follower count
        followers_count = followers.count()
        # Fetch following count for that user
        following = FollowingCount.objects.all().filter(following=profile_user.username)
        following_count = following.count()
        print("accounts followed by: ", profile_user)
        print(following)
        print(following_count)

        context = {
            'profile_username': profile_username,
            'profile_user': profile_user,
            'profile_posts': profile_posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'following_auth_user_count': following_auth_user_count,
            'alreadyFollows': alreadyFollows,
            'user': user
        }

    return render(request, "network/profile.html", context)

@login_required
def unfollow_profile(request, username):
    # Fetch information about the requested profile
    profile_username = username
    profile_user = User.objects.all().filter(username=profile_username)[0]

    # Fetch all posts for that user
    profile_posts = Post.objects.all().filter(posted_by=profile_user).order_by('-posted_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(profile_posts, 10) # show 10 posts per page

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # authentified user
    user = request.user 

    alreadyFollows = False # Unfollow button displayed

    # Fetch followers for that user
    followers = FollowersCount.objects.all().filter(profile=profile_user)

    # Fetch following count for that user
    following = FollowingCount.objects.all().filter(profile=profile_user)

    # If the user already follows the profile
    if followers.filter(follower=user).exists() == True:

        # Unfollow
        try:
            remove_follower = FollowersCount.objects.get(profile=profile_user, follower=user)
            print("Remove: ", remove_follower)
            remove_follower.delete()

            remove_following = FollowingCount.objects.get(profile=profile_user, following=user)
            print("Remove: ", remove_following)
            remove_following.delete()
        
            # Refresh follower count for that user
            followers = FollowersCount.objects.all().filter(profile=profile_user)
            followers_count = followers.count()
            print(followers)

            # Refresh following count for that user
            following = FollowingCount.objects.all().filter(following=profile_user.username)
            following_count = following.count()
            print(following)

            context = {
                'profile_username': profile_username,
                'profile_user': profile_user,
                'profile_posts': profile_posts,
                'followers_count': followers_count,
                'following_count': following_count,
                'alreadyFollows': alreadyFollows,
                'posts': posts,
                'user': user
            }

            return render(request, "network/profile.html", context)
        
        except FollowersCount.DoesNotExist:
            print("Error: FollowersCount.DoesNotExist")
        except FollowersCount.MultipleObjectsReturned:
            print("Error: FollowersCount.MultipleObjectsReturned")

    else: 
        following_count = following.count()
        print(following)

        context = {
            'profile_username': profile_username,
            'profile_user': profile_user,
            'profile_posts': profile_posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'alreadyFollows': alreadyFollows,
            'posts': posts,
            'user': user
        }

        return render(request, "network/profile.html", context)

@login_required
def following_view(request):
    # authenticated user
    user = request.user 

    # All profiles that user currently follows
    following_auth_user = FollowingCount.objects.all().filter(following=user.username).values_list('profile', flat=True)
    following_auth_user_list = list(following_auth_user)

    usersfollowed = []
    usernames = []
    postsfollowed = []

    for id in following_auth_user_list:
        postsforpersonfollowed = Post.objects.all().filter(posted_by=id).order_by('-posted_at')
        postsforpersonfollowed_list = list(postsforpersonfollowed)
        postsfollowed.append(postsforpersonfollowed_list)
    
    postsfollowed_list = [postfollowed for sublist in postsfollowed for postfollowed in sublist]
    # sort the list of posts in reverse chronological order, latest posts first
    postsfollowed_list_sorted = sorted(postsfollowed_list, key=attrgetter('posted_at'), reverse=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(postsfollowed_list_sorted, 10) # show 10 posts per page

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'user': user,
        'following_auth_user': following_auth_user,
        'following_auth_user_list': following_auth_user_list,
        'postsfollowed': postsfollowed,
        'postsfollowed_list': postsfollowed_list,
        'postsfollowed_list_sorted': postsfollowed_list_sorted,
        'posts': posts
    }

    return render(request, "network/following.html", context)

@login_required
def update_view(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        timestamp = datetime.now()
         
        if data.get("content") is not None:
            post.content = data["content"]
            post.posted_at = timestamp # Problem with format in which date is saved: "Jan 17 2022, 02:41 PM" instead of Jan. 17, 2022, 2:41 p.m.
        post.save()
        return JsonResponse(post.serialize()) # HttpResponse(status=204) This returned an error (I want to return json to display it)
    
    # Post must be via GET or PUT
    else: 
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
# https://www.youtube.com/watch?v=PXqRPqDjDgc
def like_view(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        post.likes.add(request.user)
        return JsonResponse(post.serialize())

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def unlike_view(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        post.likes.remove(request.user)
        return JsonResponse(post.serialize())

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)



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
