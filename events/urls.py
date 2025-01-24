from django.urls import path
from events.views import events,event_details,dashboard,add_event,add_participant,add_category

urlpatterns = [
    path('event/', events, name='event'),
    path('event-details/<int:id>', event_details, name='details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-event/', add_event, name='add-event'),
    path('add-participant/', add_participant, name='add-participant'),
    path('add-category/', add_category, name='add-category'),
]
