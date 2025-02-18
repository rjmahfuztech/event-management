from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_image/default-img.jpg')
    phone = models.CharField(max_length=17, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username