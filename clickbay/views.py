from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
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
            return redirect('index')
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
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html',{"message":message, "form":form})