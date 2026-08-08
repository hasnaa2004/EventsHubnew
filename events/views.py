from django.shortcuts import render
from .models import Event


def home_view(request):
    events = Event.objects.filter(
        status='available'
    ).order_by('date')

    return render(request, 'home.html', {
        'events': events,
    })


def events_list_view(request):
    events = Event.objects.filter(
        status='available'
    ).order_by('date')

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        events = events.filter(title__icontains=query)

    if category:
        events = events.filter(category=category)

    return render(request, 'events/events_list.html', {
        'events': events,
        'query': query,
        'selected_category': category,
    })


def event_detail_view(request, event_id):
    event = Event.objects.get(
        id=event_id,
        status='available'
    )

    return render(request, 'events/event_detail.html', {
        'event': event,
    })