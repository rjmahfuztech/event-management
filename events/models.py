from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default=1,
        related_name='event'
    )
    participant = models.ManyToManyField(User, related_name='event')
    image = CloudinaryField('Event Images', folder='event_images', blank=True, null=True, default='https://res.cloudinary.com/duae8oyif/image/upload/v1753288848/default-img_tprf5k.jpg')

    def __str__(self):
        return self.name
    

class Speaker(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=350)
    bio = models.TextField(blank=True)
    photo = CloudinaryField('Picture', folder='speaker_photo', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers')
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name