from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class CustomUser(AbstractUser):
    profile_image = CloudinaryField('Profile Image', folder='profile_images', blank=True, null=True, default='https://res.cloudinary.com/duae8oyif/image/upload/v1753288950/default-img_z02qp1.jpg')
    phone = models.CharField(max_length=17, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username