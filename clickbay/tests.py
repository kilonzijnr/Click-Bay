from django.test import TestCase
from .models import Image, Profile, Likes

# Create your tests here.
class ImageTest(TestCase):
    def setUp(self):
        self.profile = Profile(name='kilonzi')
        self.profile.save_profile()
        self.likes = Likes(likes=1)
        self.likes = Likes.save_likes()
        self.image_test = Image(name='dimitry', caption='Grid and Chill',
                                profile=self.profile, likes=self.likes)

    def test_instance(self):
        self.assertTrue(isinstance(self.image_test, Image))

    def test_save_image(self):
        self.image_test.save_image()
        after = Image.objects.all()
        self.assertTrue(len(after) > 0)