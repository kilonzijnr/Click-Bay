from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
# Create your views here.

def user_login(request):
    """Function for user login"""

    message = 'KINDLY LOGIN TO PROCEED'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request,f" Hey {username} Welcome to Click Bay!")
            return redirect('homepage')
        else:
            messages.success(request,"Something went wrong Kindly try to Login again")
            return render(request,'reqistration/login.html')
    else:
        return render(request, 'registration/login.html',{"message":message})

def user_logout(request):
    """Function for signing out of the application"""

    logout(request)
    messages.success(request,("Signout Succesfull"))
    return redirect('login')

def user_signup(request):
    """Function for reqistering a new application user account"""

    message = 'CREATE YOUR ACCOUNT HERE!'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,("Account created succesfully!"))
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html',{"message":message, "form":form})

def homepage(request):
    """Display function for all images"""
    images = Image.objects.all()
    return render(request, 'home.html', {"images":images})

def profile(request):
    """Display function for user profile"""
    current_user = request.user
    images = Image.objects.filter(user_id=current_user.id)
    profile = Profile.objects.filter(username=current_user).first()
    return render(request,'profile.html', {"images":images, "profile":profile})

def like_image(request, id):
    """Display function for Image Likes"""
    likes = Likes.objects.filter(image_id=id).first()
    if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():
        likes.delete()
        image = Image.objects.get(id=id)
        if image.total_likes == 0:
            image.total_likes = 0
            image.save()
        else:
            image.total_likes -= 1
            image.save()
        return redirect('/')
    else:
        likes = Likes(image_id=id, user_id=request.user.id)
        likes.save()
        image = Image.objects.get(id=id)
        image.total_likes = image.total_liks +1
        image.save()
        return redirect('/')

def image_comments(request, id):
    """Display function for image comments"""
    image = Image.objects.get(id=id)
    related_images = Image.objects.filter(user_id=image.user_id)
    title = image.name
    if Image.objects.filter(id=id).exists():
        comments = Comments.objects.filter(image_id=id)
        return render(request,'photos.html',
        {'image':image, 
        'comments':comments, 
        'images':related_images,
        'title':title}) 
    else:
        return redirect('/')


