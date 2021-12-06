# Generated by Django 3.2.9 on 2021-12-06 10:49

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clickbay', '0006_image_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profilephoto',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]