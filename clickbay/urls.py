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
    path('profile/update/', views.update_profile, name='update_profile'),
    path('user/<int:id>/', views.user_profile, name='user_profile'),
    path('like/<int:id>/', views.like_image, name='like_image'),
    path('comment/add', views.save_comment, name='add_comment'),
    path('^search/', views.search_images, name='search_images'),
    path('upload/add/', views.save_image, name='save.image'),
    path('picture/<int:id>/', views.image_comments, name='single_image'),
    path('follow/<int:pk>',views.FollowView,name="follow")
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)