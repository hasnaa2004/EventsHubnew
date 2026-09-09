
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from .models import Event, Notification
from .forms import EventForm

from .filters import (
    EVENT_CATEGORIES,
    EVENT_STATUS,
    EVENT_TYPES,
    EVENT_CITIES,
    SORT_OPTIONS,
    find_category,
    matches_search,
    normalize_text,
)


# =========================================================
# الصفحة الرئيسية
# =========================================================

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


# =========================================================
# قائمة الفعاليات + البحث والفلاتر
# =========================================================

def event_list_view(request):

    events = Event.objects.all()

    # -----------------------------------------------------
    # قراءة قيم البحث والفلاتر
    # -----------------------------------------------------

    query = request.GET.get(
        "q",
        ""
    ).strip()

    category = request.GET.get(
        "category",
        "all"
    )

    status = request.GET.get(
        "status",
        "all"
    )

    event_type = request.GET.get(
        "event_type",
        "all"
    )

    city = request.GET.get(
        "city",
        "all"
    )

    sort = request.GET.get(
        "sort",
        "newest"
    )

    # -----------------------------------------------------
    # فلتر التصنيف
    # -----------------------------------------------------

    category = find_category(category)

    if category != "all":

        events = events.filter(
            category=category
        )

    # -----------------------------------------------------
    # فلتر الحالة
    # -----------------------------------------------------

    if status != "all":

        events = events.filter(
            status=status
        )

    # -----------------------------------------------------
    # فلتر نوع الفعالية
    # -----------------------------------------------------

    if event_type != "all":

        events = events.filter(
            event_type=event_type
        )

    # -----------------------------------------------------
    # فلتر المدينة
    # -----------------------------------------------------

    if city != "all":

        events = events.filter(
            city=city
        )

    # -----------------------------------------------------
    # البحث الذكي
    # عربي + إنجليزي + أكثر من كلمة
    # -----------------------------------------------------

    if query:

        search_query = normalize_text(
            query
        )

        matched_events = []

        for event in events:

            searchable_text = " ".join(
                [
                    str(event.title or ""),
                    str(event.description or ""),
                    str(event.location or ""),
                    str(event.city or ""),
                    str(event.category or ""),
                    str(event.event_type or ""),
                ]
            )

            if matches_search(
                searchable_text,
                search_query
            ):

                matched_events.append(
                    event
                )

        events = matched_events

    # -----------------------------------------------------
    # ترتيب النتائج
    # -----------------------------------------------------

    if sort == "newest":

        if hasattr(events, "order_by"):

            events = events.order_by(
                "-date"
            )

        else:

            events.sort(
                key=lambda event: event.date,
                reverse=True
            )

    elif sort == "oldest":

        if hasattr(events, "order_by"):

            events = events.order_by(
                "date"
            )

        else:

            events.sort(
                key=lambda event: event.date
            )

    elif sort == "price_high":

        if hasattr(events, "order_by"):

            events = events.order_by(
                "-price"
            )

        else:

            events.sort(
                key=lambda event: event.price or 0,
                reverse=True
            )

    elif sort == "price_low":

        if hasattr(events, "order_by"):

            events = events.order_by(
                "price"
            )

        else:

            events.sort(
                key=lambda event: event.price or 0
            )

    # -----------------------------------------------------
    # البيانات المرسلة إلى القالب
    # -----------------------------------------------------

    context = {

        "events": events,

        "categories": EVENT_CATEGORIES,

        "statuses": EVENT_STATUS,

        "event_types": EVENT_TYPES,

        "cities": EVENT_CITIES,

        "sort_options": SORT_OPTIONS,

        # البحث
        "query": query,

        # الفلاتر المختارة
        "selected_category": category,

        "selected_status": status,

        "selected_type": event_type,

        "selected_city": city,

        "selected_sort": sort,

        # معلومات المشروع
        "developer": "المهندسة حسناء",

        "course_name": "Software Engineering",

        "year": 2026,
    }

    return render(
        request,
        "events/event_list.html",
        context
    )


# =========================================================
# تفاصيل الفعالية
# =========================================================

@login_required
def event_detail_view(
    request,
    event_id
):

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


# =========================================================
# إضافة فعالية
# =========================================================

@login_required
@permission_required(
    "events.add_event",
    raise_exception=True
)
def event_create_view(request):

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            # ---------------------------------------------
            # تجهيز الفعالية
            # ---------------------------------------------

            event = form.save(
                commit=False
            )

            # المستخدم الذي أنشأ الفعالية
            event.created_by = request.user

            # حفظ الفعالية
            # عند الحفظ يعمل post_save تلقائيًا
            event.save()

            # ---------------------------------------------
            # رسالة نجاح داخل الموقع
            # ---------------------------------------------

            messages.success(
                request,
                "تمت إضافة الفعالية بنجاح، "
                "وسيتم إرسال الإشعار والبريد الإلكتروني."
            )

            return redirect(
                "event_list"
            )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    else:

        form = EventForm()

    return render(
        request,
        "events/event_form.html",
        {
            "form": form
        }
    )


# =========================================================
# عرض إشعارات المستخدم الحالي
# =========================================================

@login_required
def notification_list_view(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "events/notifications.html",
        {
            "notifications": notifications,

            "developer": "المهندسة حسناء",

            "course_name": "Software Engineering",

            "year": 2026,
        }
    )


# =========================================================
# تعليم إشعار كمقروء
# =========================================================

@login_required
def notification_read_view(
    request,
    notification_id
):

    # يسمح بالتعديل باستخدام POST فقط
    if request.method == "POST":

        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user
        )

        notification.is_read = True

        notification.save(
            update_fields=[
                "is_read"
            ]
        )

    return redirect(
        "notification_list"
    )
