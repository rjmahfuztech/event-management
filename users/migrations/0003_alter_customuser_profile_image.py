# Generated by Django 5.1.5 on 2025-07-26 19:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/duae8oyif/image/upload/v1753288950/default-img_z02qp1.jpg', max_length=255, null=True, verbose_name='Profile Image'),
        ),
    ]
