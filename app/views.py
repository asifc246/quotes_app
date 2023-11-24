from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from .forms import tweetForm,SignUpForm,ProfilePicForm,UpdateUserForm
from django.contrib.auth import authenticate,login,logout
from django import forms
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = tweetForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                tweetobj = form.save(commit=False)
                tweetobj.user = request.user
                tweetobj.save()
                return redirect('home')
        tweet = Tweet.objects.all().order_by("-created_at")
        context = {'tweet':tweet,'form':form}
        return render(request,'home.html',context)
    else:
        tweet = Tweet.objects.all().order_by("-created_at")
        context = {'tweet':tweet}
        return render(request,'home.html',context)

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context = {}
        context['data'] = profiles
        print(context)
        return render(request,'profile_list.html',context)
    else:
        messages.success(request,("You Must Log in to View"))
        return redirect('home')
    
def profile(request,id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = id)
        tweet = Tweet.objects.filter(user=id).order_by("-created_at")
        context = {'profile':profile,'tweet':tweet}
        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)

            current_user_profile.save()
        return render(request,'profile.html',context)
    else:
        messages.success(request, ("You Must Log in to View"))
        return redirect("home")
    
def followers(request,id):
    if request.user.is_authenticated:
        if request.user.id == id:
            profiles = Profile.objects.get(user_id=id)
            context = {'profiles':profiles}
            return render(request,'followers.html',context)
        else:
            messages.success(request,("Thats not your profile"))
            return redirect('home')
    else:
        messages.success(request,("You Must Log in to View"))
        return redirect('home')
    
def following(request,id):
    if request.user.is_authenticated:
        if request.user.id == id:
            profiles = Profile.objects.get(user_id=id)
            context = {'profiles':profiles}
            return render(request,'following.html',context)
        else:
            messages.success(request,("Thats not your profile"))
            return redirect('home')
    else:
        messages.success(request,("You Must Log in to View"))
        return redirect('home')
        

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,(f"Welcome To Quotes {user.username}"))
            return redirect('home')
        else:
            messages.success(request,("There was an error logging in please try again"))
            return redirect('login')
    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,("Successfully logged out from quotes"))
    return redirect('login')

def register_user(request):
    user_form = SignUpForm()
    context = {'user_form':user_form}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You Have Successfuly Registered in Quotes"))
            return redirect('home')
    return render(request,'register.html',context)

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        # Get Forms
        user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ("Your Profile Has Been Updated!"))
            return redirect('home')

        return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')

def tweet_likes(request,id):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet,id=id)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request,("You Must Be logged in to access"))
        return redirect('home')

def tweet_share(request,id):
    tweet = get_object_or_404(Tweet,id=id)
    context = {'i':tweet}
    if tweet:
        return render(request,'share_tweet.html',context)
    else:
        messages.success(request,("Quote doen't exist in our server"))
        return redirect('home')
    
def unfollow(request,id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=id)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request,(f"You have succesfully unfollowed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request,("Access is limited to logged in users"))
        return redirect('home')
    
def follow(request,id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=id)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request,("You have succesfully followed {profile.user.username}"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request,("Access is limited to logged in users"))
        return redirect('home')
    
def delete_tweet(request,id):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet,id=id)
        if request.user.username == tweet.user.username:
            tweet.delete()
            messages.success(request,("Successfully deleted"))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request,("Access is limited to authorised users"))
            return redirect('home')
    else:
        messages.success(request,("Please login to continue"))
        return redirect('home')

def edit_tweet(request,id):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet,id=id)
        if request.user.username == tweet.user.username:
            form = tweetForm(request.POST or None, instance=tweet)
            context = {'form':form,'i':tweet}
            if request.method == "POST":
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request,('Updated successfully'))
                    return redirect('home')
            else:
                return render(request,'edit_tweet.html',context)
        else:
            messages.success(request,('Access is limited to authorised users'))
            return redirect('home')
    else:
        messages.success(request,("Please login to continue"))
        return redirect('home')
    
def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        searched = Tweet.objects.filter(body__contains = search)
        return render(request,'search.html',{'search':searched})
    else:
        return render(request,'search.html')
    
def search_user(request):
    if request.method == 'POST':
        search = request.POST['search']
        searched = User.objects.filter(username__contains = search)
        return render(request,'search_user.html',{'search':searched})
    else:
        return render(request,'search_user.html')
    