from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField
from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    """Model class for handling user profile"""

    profilephoto = CloudinaryField('image')
    bio = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    signup_date = models.DateTimeField(auto_now_add= True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return self.username

    def total_followers(self):
        """Method to return total number or user followers"""
        return self.followers.count()

    def save_profile(self):
        self.save()

    def update_profile(self, new):
        """Method to update user profile details
        Args:
            new([type]): [description]
        """

        self.username = new.username
        self.bio = new.bio
        self.profilephoto = new.profilephoto
        self.save()

    @classmethod
    def get_following(cls, user):
        """Method to get all number of user followings"""
        following = user.followers.all()
        users = []
        for profile in following:
            user = user.objects.get(profile = profile)
            users.append(user)
        return users

    @classmethod
    def search_profile(cls, search_term):
        """Method to enable search functionality which returns specific user profile"""
        profiles = cls.objects.filter(username_icontains = search_term)
        return profiles
    
class Image(models.Model):
    """Model for handling photo posts by users"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField('images')
    image_name = models.CharField(max_length=25)
    image_caption = models.CharField(max_length=150)
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    comment = models.CharField(max_length=150 )
    post_time = models.DateTimeField(auto_now_add = True)
    total_comments = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)

    class Meta:
         ordering = ['-post_time']

    def __str__(self):
        return self.imagename

    def save_image(self):
        """Method for saving images"""
        self.save()

    def delete_image(self):
        """Method for deleting image"""
        self.delete()

    def like_image(self, user):
        """Method for adding user"""
        self.likes.add(user)

    def gettottal_likes(self):
        """Method for getting total number of image likes"""
        return self.likes.count()

    def update_caption(self, caption):
        """Method to update captions for images"""
        self.caption = caption
        self.save()

    @classmethod
    def get_images(cls, users):
        """Method for sourcing for a specific image"""
        posts = []
        for user in users:
            images = Image.objects.filter(user = user)
            for image in images:
                posts.append(image)
        return posts

    @classmethod
    def get_comments(self):
        """Method for sourcing for image comments"""
        comments = Comments.objects.filter(image = self)
        return comments

    @classmethod
    def search_by_image_name(cls, search_term):
        posts = cls.objects.filter(
            image_name__icontains=search_term)
        return posts
class Comments(models.Model):
    """Model class for image comments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()


class Likes(models.Model):
    """Model for handling likes on an image"""
    
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    




