from django.urls import path
from events.views import events_info,event_details,dashboard,add_event,add_category,category,participant,event,update_event,delete_event,delete_participant,update_category,delete_category


urlpatterns = [
    path('', events_info, name='event-info'),
    path('event-details/<int:id>', event_details, name='details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('category/', category, name='category'),
    path('add-category/', add_category, name='add-category'),
    path('update-category/<int:id>', update_category, name='update-category'),
    path('delete-category/<int:id>', delete_category, name='delete-category'),
    path('event/', event, name='event'),
    path('add-event/', add_event, name='add-event'),
    path('update-event/<int:id>', update_event, name='update-event'),
    path('delete-event/<int:id>', delete_event, name='delete-event'),
    path('participant/', participant, name='participant'),
    path('delete-participant/<int:id>', delete_participant, name='delete-participant'),
]
