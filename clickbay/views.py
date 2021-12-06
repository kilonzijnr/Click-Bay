from os import name
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
import cloudinary.api
import cloudinary.uploader
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def user_login(request):
    """Function for user login"""

    message = 'Sign In!'
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
            return render(request,'registration/login.html')
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
    images = Image.objects.filter(profile_id=current_user.id)
    profile = Profile.objects.filter(username=current_user).first()
    return render(request,'profile.html', {"images":images, "profile":profile})

def like_image(request, id):
    """Display function for Image Likes"""
    likes = Likes.objects.filter(image_id=id).first()
    if Likes.objects.filter(image_id=id, profile_id=request.profile.id).exists():
        likes.delete()
        image = Image.objects.get(id=id)
        if image.total_likes == 0:
            image.total_likes = 0
            image.save()
        else:
            image.total_likes += 1
            image.save()
        return redirect('homepage')
    else:
        likes = Likes(image_id=id, profile_id=request.user.id)
        likes.save()
        image = Image.objects.get(id=id)
        image.total_likes = image.total_likes +1
        image.save()
        return redirect('homepage')

def image_comments(request, id):
    """Display function for image comments"""
    image = Image.objects.get(id=id)
    related_images = Image.objects.filter(profile_id=image.profile_id)
    title = image.imagename
    if Image.objects.filter(id=id).exists():
        comments = Comments.objects.filter(image_id=id)
        return render(request,'photos.html',
        {'image':image, 
        'comments':comments, 
        'images':related_images,
        'title':title}) 
    else:
        return redirect('/')

def save_comment(request):
    """Display function for saving image comments"""
    if request.method == 'POST':
        comment = request.POST['comment']
        image_id = request.POST['image_id']
        image = Image.objects.get(id=image_id)
        user = request.user
        comment = Comments(comment=comment, image_id=image_id, profile_id=user.id)
        comment.save_comment()
        image.total_comments = image.total_comments + 1
        image.save()
        return redirect('homepage')

def user_profile(request,id):
    """Display function for filtering a specific user"""
    if User.objects.filter(id=id).exists():
        user = User.objects.get(id=id)
        images = Image.objects.filter(user_id=id)
        followers = Profile.total_followers()
        profile = Profile.objects.filter(username_id=id).first()
        return render(request,'user.html',{'images':images,'profile':profile, 'user':user, 'followers':followers})
    else:
        return redirect('/')

def search_images(request):
    """View functtion for searching for images"""
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get ('search').lower()
        images = Image.search_by_image(search_term)
        message = f'{search_term}'
        title = message

        return render(request, 'search.html', {'success':message, 'images':images, "title":title})
    else:
        message = 'Invalid Search'
        return render(request,'search.html',{'danger':message})

def update_profile(request):
    """Function for updating the user profile"""
    if request.method =='POST':
        current_user = request.user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        bio = request.POST['bio']
        profile_image = request.FILES['profilephoto']
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image['url']

        user = User.objects.get(id=current_user.id)

        if Profile.objects.filter(username_id=current_user.id).exists():
            profile = Profile.objects.get(username_id=current_user.id)
            profile.photo = profile_url
            profile.bio = bio
            profile.save()
        else:
            profile = Profile.objects.get(username_id=current_user.id, photo=profile_url, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        return redirect('/profile',{'success': 'Profile Update Successfull'})
    else:
        return render(request,'profile.html',{'danger': 'Profile update Failed'})

def save_image(request):
    """Function for saving image"""
    if request.method == 'POST':
        image_name = request.POST['image_name']
        image_caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        image_file = cloudinary.uploader.upload(image_file)
        image_url = image_file['url']
        image = Image(image_name=image_name,image_caption=image_caption,image=image_url,profile_id=request.POST['profile_id'], user_id=request.POST['user_id'])
        print(image)
        image.save_image()
        return redirect('/',{'success': 'Image Upload Successful'})
    else:
        return render(request,'profile.html', {'danger': 'Image upload Failed'})

def FollowView(request,pk):
    """This handles liking a profile
    Args:
        request ([type]): [description]
        pk ([type]): [description]
    """
    profile = get_object_or_404(Profile, pk = request.POST['profile_pk'])
    profile.followers.add(request.user)
    pk = profile.user.pk
    return HttpResponseRedirect(reverse('profile', args=[str(pk)]))
