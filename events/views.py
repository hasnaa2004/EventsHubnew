from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from .models import Event

from .filters import (
    EVENT_CATEGORIES,
    EVENT_STATUS,
    EVENT_TYPES,
    EVENT_CITIES,
    SORT_OPTIONS,
    get_category_name,
    get_status_name,
    get_type_name,
    get_city_name,
    find_category,
)


def home_view(request):

    context = {
        "course_name": "Software Engineering",
        "developer": "المهندسة حسناء",
        "university": "University",
        "semester": "Second Semester",
        "year": 2026,
    }

    return render(
        request,
        "events/home.html",
        context
    )


def events_list_view(request):

    events = Event.objects.all()

    # ==============================
    # قراءة قيم الفلتر من الرابط
    # ==============================

    category = request.GET.get("category", "all")
    status = request.GET.get("status", "all")
    event_type = request.GET.get("event_type", "all")
    city = request.GET.get("city", "all")
    sort = request.GET.get("sort", "newest")

    # ==============================
    # فلتر التصنيف
    # ==============================

    category = find_category(category)

    if category != "all":
        events = events.filter(category=category)

    # ==============================
    # فلتر الحالة
    # ==============================

    if status != "all":
        events = events.filter(status=status)

    # ==============================
    # فلتر نوع الفعالية
    # ==============================

    if event_type != "all":
        events = events.filter(event_type=event_type)

    # ==============================
    # فلتر المدينة
    # ==============================

    if city != "all":
        events = events.filter(city=city)

    # ==============================
    # الترتيب
    # ==============================

    if sort == "newest":
        events = events.order_by("-date")

    elif sort == "oldest":
        events = events.order_by("date")

    elif sort == "price_high":
        events = events.order_by("-price")

    elif sort == "price_low":
        events = events.order_by("price")

    context = {

        "events": events,

        "categories": EVENT_CATEGORIES,
        "statuses": EVENT_STATUS,
        "event_types": EVENT_TYPES,
        "cities": EVENT_CITIES,
        "sort_options": SORT_OPTIONS,

        "selected_category": category,
        "selected_status": status,
        "selected_event_type": event_type,
        "selected_city": city,
        "selected_sort": sort,

        "developer": "المهندسة حسناء",
        "course_name": "Software Engineering",
        "year": 2026,
    }

    return render(
        request,
        "events/event_list.html",
        context
    )


def event_detail_view(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    context = {
        "event": event,
        "developer": "المهندسة حسناء",
        "course_name": "Software Engineering",
        "year": 2026,
    }

    return render(
        request,
        "events/event_detail.html",
        context
    )