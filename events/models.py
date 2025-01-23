from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default="Corporate Events",
        related_name='event'
    )

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    event = models.ManyToManyField(Event, related_name='participant')