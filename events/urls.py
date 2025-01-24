from django.urls import path
from events.views import home,event_details,dashboard,add_event

urlpatterns = [
    path('home/', home),
    path('details/', event_details),
    path('dashboard/', dashboard),
    path('add-event/', add_event)
]
