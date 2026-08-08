from django.urls import path
from .views import (
    home_view,
    events_list_view,
    event_detail_view,
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

]