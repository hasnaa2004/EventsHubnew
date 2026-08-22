from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count

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
from .forms import EventForm, EventSearchForm, get_event_modelformset
from django.forms import modelformset_factory
from django.contrib.auth.models import User


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
    # base queryset with prefetch to reduce DB hits when displaying attendees
    events = Event.objects.all().prefetch_related('attendees')

    # search form (uses django.forms.Form)
    search_form = EventSearchForm(request.GET or None)
    if search_form.is_valid():
        q = search_form.cleaned_data.get('q')
        if q:
            events = events.filter(title__icontains=q)

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

    # exclude cancelled if requested (uses exclude())
    if request.GET.get('hide_cancelled') == '1':
        events = events.exclude(status='cancelled')

    # annotate attendee counts (uses annotate + Count)
    events = events.annotate(attendee_count=Count('attendees', distinct=True))

    # compute distinct cities and categories used on site (uses values() + distinct())
    distinct_cities = Event.objects.values('city').distinct()
    distinct_categories = Event.objects.values('category').distinct()

    query = ''
    if search_form.is_valid():
        query = search_form.cleaned_data.get('q') or ''

    context = {

        "events": events,
        "search_form": search_form,
        "query": query,

        "categories": EVENT_CATEGORIES,
        "statuses": EVENT_STATUS,
        "event_types": EVENT_TYPES,
        "cities": EVENT_CITIES,
        "distinct_cities": distinct_cities,
        "distinct_categories": distinct_categories,
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
        "events/events_list.html",
        context
    )


@login_required
def register_toggle(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method != 'POST':
        return redirect('event_detail', event_id=event.id)

    user = request.user

    is_registered = event.attendees.filter(id=user.id).exists()

    try:
        if not is_registered:
            event.attendees.add(user)
            messages.success(request, 'تم تسجيلك في الفعالية')
            # send notification email (will use EMAIL settings from env)
            try:
                send_mail(
                    subject=f'تم التسجيل في {event.title}',
                    message=f'شكراً لتسجيلك في {event.title}.',
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
        else:
            event.attendees.remove(user)
            messages.success(request, 'تم إلغاء تسجيلك من الفعالية')
    except Exception as e:
        messages.error(request, 'حدث خطأ أثناء معالجة طلبك')

    return redirect('event_detail', event_id=event.id)


def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    user_registered = False
    if request.user.is_authenticated:
        user_registered = event.attendees.filter(id=request.user.id).exists()

    context = {
        "event": event,
        "user_registered": user_registered,
        "developer": "المهندسة حسناء",
        "course_name": "Software Engineering",
        "year": 2026,
    }

    return render(request, 'events/event_detail.html', context)


def staff_required(user):
    return user.is_active and user.is_staff


@login_required
@user_passes_test(staff_required)
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'تم إنشاء الفعالية بنجاح')
            return redirect('event_detail', event_id=event.id)
        else:
            messages.error(request, 'هناك أخطاء، أصلحها ثم أعد المحاولة')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form, 'action': 'إنشاء'})


@login_required
@user_passes_test(staff_required)
def update_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الفعالية')
            return redirect('event_detail', event_id=event.id)
        else:
            messages.error(request, 'هناك أخطاء في النموذج')
    else:
        form = EventForm(instance=event)

    return render(request, 'event_form.html', {'form': form, 'action': 'تعديل'})


@login_required
@user_passes_test(staff_required)
def delete_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'تم حذف الفعالية')
        return redirect('events_list')

    return render(request, 'events/event_confirm_delete.html', {'event': event})


@login_required
@user_passes_test(staff_required)
def bulk_events_view(request):
    EventFormSet = get_event_modelformset(extra=3)
    queryset = Event.objects.none()
    if request.method == 'POST':
        formset = EventFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            instances = formset.save()
            messages.success(request, 'تم إنشاء الفعاليات بنجاح')
            return redirect('events_list')
    else:
        formset = EventFormSet(queryset=queryset)

    return render(request, 'events/event_bulk_form.html', {'formset': formset})