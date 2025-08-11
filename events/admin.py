from django.contrib import admin
from events.models import Event, Category, Speaker

# Register your models here.
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Speaker)