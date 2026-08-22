from django.urls import path
from .views import (
    home_view,
    events_list_view,
    event_detail_view,
    register_toggle,
    create_event_view,
    update_event_view,
    delete_event_view,
    bulk_events_view,
)

urlpatterns = [

    path(
        '',
        home_view,
        name='home'
    ),

    path(
        'events/',
        events_list_view,
        name='events_list'
    ),

    path(
        'events/<int:event_id>/',
        event_detail_view,
        name='event_detail'
    ),
    path(
        'events/<int:event_id>/register/',
        register_toggle,
        name='event_register'
    ),
    path('events/create/', create_event_view, name='event_create'),
    path('events/bulk-create/', bulk_events_view, name='events_bulk_create'),
    path('events/<int:event_id>/edit/', update_event_view, name='event_edit'),
    path('events/<int:event_id>/delete/', delete_event_view, name='event_delete'),

]