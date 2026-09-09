
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage


# =========================================================
# تسجيل الدخول
# =========================================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'تم تسجيل الدخول بنجاح'
            )

            return redirect('home')

        messages.error(
            request,
            'اسم المستخدم أو كلمة المرور غير صحيحة'
        )

        return render(
            request,
            'account/login.html'
        )

    return render(
        request,
        'account/login.html'
    )


# =========================================================
# إنشاء حساب
# =========================================================

def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'اسم المستخدم موجود مسبقاً'
            )

            return render(
                request,
                'account/register.html'
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        messages.success(
            request,
            'تم إنشاء الحساب وتسجيل الدخول بنجاح'
        )

        return redirect('home')

    return render(
        request,
        'account/register.html'
    )


# =========================================================
# الملف الشخصي
# =========================================================

@login_required
def profile_view(request):

    return render(
        request,
        'account/profile.html'
    )


# =========================================================
# لوحة التحكم
# =========================================================

@login_required
def dashboard_view(request):

    return render(
        request,
        'account/dashboard.html'
    )


# =========================================================
# تسجيل الخروج
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'تم تسجيل الخروج بنجاح'
    )

    return redirect('home')


# =========================================================
# إرسال رسالة 
# باستخدام EmailMessage
# =========================================================

from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


@login_required
def contact_engineer_view(request):

    # -------------------------------------------------
    # جميع المستخدمين المسجلين
    # نستبعد المستخدم الحالي من قائمة المستلمين
    # -------------------------------------------------

    registered_users = User.objects.exclude(
        id=request.user.id
    ).exclude(
        email=""
    ).order_by(
        "username"
    )

    if request.method == "POST":

        # -------------------------------------------------
        # المستخدمون المختارون من الموقع
        # -------------------------------------------------

        selected_user_ids = request.POST.getlist(
            "recipient_users"
        )

        # -------------------------------------------------
        # البريد اليدوي
        # يمكن إدخال أكثر من بريد
        # -------------------------------------------------

        manual_emails_text = request.POST.get(
            "manual_emails",
            ""
        ).strip()

        # -------------------------------------------------
        # الموضوع
        # -------------------------------------------------

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        # -------------------------------------------------
        # نص الرسالة
        # -------------------------------------------------

        message_text = request.POST.get(
            "message",
            ""
        ).strip()

        # -------------------------------------------------
        # قائمة المستلمين النهائية
        # -------------------------------------------------

        recipients = []

        # -------------------------------------------------
        # إضافة إيميلات المستخدمين المسجلين
        # -------------------------------------------------

        if selected_user_ids:

            users = User.objects.filter(
                id__in=selected_user_ids
            ).exclude(
                email=""
            )

            for user in users:

                if user.email not in recipients:
                    recipients.append(
                        user.email
                    )

        # -------------------------------------------------
        # إضافة الإيميلات المدخلة يدويًا
        #
        # يقبل:
        # email1@gmail.com
        # email2@gmail.com, email3@gmail.com
        # -------------------------------------------------

        if manual_emails_text:

            manual_emails = manual_emails_text.replace(
                ",",
                "\n"
            ).splitlines()

            for email in manual_emails:

                email = email.strip()

                if email and email not in recipients:
                    recipients.append(email)

        # -------------------------------------------------
        # التحقق من المستلمين
        # -------------------------------------------------

        if not recipients:

            messages.error(
                request,
                "يرجى اختيار مستخدم واحد على الأقل "
                "أو إدخال بريد إلكتروني واحد على الأقل."
            )

            return render(
                request,
                "account/contact.html",
                {
                    "registered_users": registered_users
                }
            )

        # -------------------------------------------------
        # التحقق من الموضوع
        # -------------------------------------------------

        if not subject:

            messages.error(
                request,
                "يرجى كتابة موضوع الرسالة."
            )

            return render(
                request,
                "account/contact.html",
                {
                    "registered_users": registered_users
                }
            )

        # -------------------------------------------------
        # التحقق من محتوى الرسالة
        # -------------------------------------------------

        if not message_text:

            messages.error(
                request,
                "يرجى كتابة نص الرسالة."
            )

            return render(
                request,
                "account/contact.html",
                {
                    "registered_users": registered_users
                }
            )

        # -------------------------------------------------
        # إنشاء البريد
        # -------------------------------------------------

        email = EmailMessage(

            subject=subject,

            body=(
                "رسالة من منصة EventHub\n"
                "--------------------------------\n\n"

                f"اسم المرسل: {request.user.username}\n"

                f"بريد المرسل: {request.user.email}\n\n"

                "الرسالة:\n"

                f"{message_text}\n"
            ),

            from_email=None,

            to=recipients,
        )

        # -------------------------------------------------
        # إرسال البريد
        # -------------------------------------------------

        email.send(
            fail_silently=False
        )

        # -------------------------------------------------
        # رسالة نجاح
        # -------------------------------------------------

        messages.success(
            request,
            f"تم إرسال الرسالة بنجاح إلى "
            f"{len(recipients)} مستلم/مستلمين."
        )

        return redirect(
            "contact_engineer"
        )

    # -------------------------------------------------
    # GET
    # -------------------------------------------------

    return render(
        request,
        "account/contact.html",
        {
            "registered_users": registered_users
        }
    )
