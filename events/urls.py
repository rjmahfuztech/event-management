from django.urls import path
from events.views import events_info, event_list, dashboard,add_event,add_category,category,participant,event,delete_event,delete_participant,update_category,delete_category, join_in_event,user_booked_events, CustomEventDetailsView, CustomUpdateEventView


urlpatterns = [
    path('', events_info, name='event-info'),
    path('event-list', event_list, name='event-list'),
    path('event-details/<int:id>/', CustomEventDetailsView.as_view(), name='details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('category/', category, name='category'),
    path('add-category/', add_category, name='add-category'),
    path('update-category/<int:id>/', update_category, name='update-category'),
    path('delete-category/<int:id>/', delete_category, name='delete-category'),
    path('event/', event, name='event'),
    path('add-event/', add_event, name='add-event'),
    path('update-event/<int:id>/', CustomUpdateEventView.as_view(), name='update-event'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
    path('users/admin/participant/', participant, name='participant'),
    path('delete-participant/<int:id>', delete_participant, name='delete-participant'),
    path('join-in-event/<int:id>/', join_in_event, name='join-event'),
    path('users/my-event/', user_booked_events, name='my-event')
]
