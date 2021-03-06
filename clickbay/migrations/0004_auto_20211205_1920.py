# Generated by Django 3.2.9 on 2021-12-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickbay', '0003_rename_image_name_image_imagename'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-post_time']},
        ),
        migrations.RenameField(
            model_name='image',
            old_name='time_posted',
            new_name='post_time',
        ),
        migrations.AddField(
            model_name='image',
            name='total_comments',
            field=models.IntegerField(default=0),
        ),
    ]
