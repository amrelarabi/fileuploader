# Generated by Django 2.2 on 2020-11-15 01:23

from django.db import migrations, models
import uploader.models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0004_auto_20201115_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=uploader.models.user_directory_path),
        ),
    ]
