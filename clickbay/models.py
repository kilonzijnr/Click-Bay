from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField

# Create your models here.

class Profile(models.Model):
    """Model class for handling user profile"""

    profilephoto = ImageField('image')
    bio = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    signup_date = models.DateTimeField(auto_now_add= True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    
