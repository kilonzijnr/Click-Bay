from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
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
