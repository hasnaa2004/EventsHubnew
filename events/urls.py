from django.urls import path

from .views import (
    event_list_view,
    event_detail_view,
    event_create_view,
    notification_list_view,
    notification_read_view,
)


urlpatterns = [

    path(
        'events/',
        event_list_view,
        name='event_list'
    ),

    path(
        'events/<int:event_id>/',
        event_detail_view,
        name='event_detail'
    ),

    path(
        'create/',
        event_create_view,
        name='event_create'
    ),

    path(
        'notifications/',
        notification_list_view,
        name='notification_list'
    ),

    path(
        'notifications/<int:notification_id>/read/',
        notification_read_view,
        name='notification_read'
    ),
]