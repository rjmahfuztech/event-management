from django.urls import path
from events.views import hello

urlpatterns = [
    path('hello/', hello)
]
