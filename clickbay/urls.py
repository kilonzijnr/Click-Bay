from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import *

# Application Views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('profile', profile, name='profile'),
    path('homepage', homepage, name='homepage'),
]