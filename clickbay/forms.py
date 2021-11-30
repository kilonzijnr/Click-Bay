from django.db.models import fields
from django.forms import ModelForm
from . models import Image, Profile

# Create your forms here

class CreatePostForm(ModelForm):
    """A form for creating a new post"""

    class meta:
        model = Image
        fields = '__all__'
        exclude = ['likes', 'user']