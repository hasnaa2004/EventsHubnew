
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import Event, Notification


# =========================================================
# Signal عند إنشاء فعالية جديدة
# =========================================================

@receiver(post_save, sender=Event)
def event_saved(sender, instance, created, **kwargs):

    # يعمل فقط عند إنشاء فعالية جديدة
    if not created:
        return

    # يجب أن يكون هناك مستخدم أنشأ الفعالية
    if not instance.created_by:
        return

    # =====================================================
    # إنشاء الإشعار داخل قاعدة البيانات
    # =====================================================

    Notification.objects.create(
        recipient=instance.created_by,
        message=(
            f'تمت إضافة الفعالية "{instance.title}" بنجاح.'
        )
    )

    # =====================================================
    # إرسال البريد بعد نجاح الـ transaction
    # =====================================================

    if instance.created_by.email:

        def send_event_email():

            # -------------------------------------------------
            # الرسالة النصية البديلة
            # -------------------------------------------------

            text_content = (
                f"مرحبًا {instance.created_by.username}،\n\n"
                f"تمت إضافة فعاليتك بنجاح إلى منصة EventHub.\n\n"
                f"اسم الفعالية: {instance.title}\n"
                f"التاريخ: {instance.date}\n"
                f"الموقع: {instance.location}\n"
                f"السعر: {instance.price}\n\n"
                f"شكرًا لاستخدامك EventHub."
            )

            # -------------------------------------------------
            # الرسالة HTML
            # -------------------------------------------------

            html_content = f"""
            <html>
            <body dir="rtl" style="
                font-family: Arial, sans-serif;
                background-color: #f5f7fa;
                padding: 30px;
            ">

                <div style="
                    max-width: 650px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 18px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                ">

                    <h2 style="
                        margin-bottom: 20px;
                    ">
                        🎉 تمت إضافة الفعالية بنجاح
                    </h2>

                    <p>
                        مرحبًا
                        <strong>{instance.created_by.username}</strong>،
                    </p>

                    <p>
                        تم تسجيل فعاليتك بنجاح في منصة
                        <strong>EventHub</strong>.
                    </p>

                    <div style="
                        background: #f1f5f9;
                        padding: 20px;
                        border-radius: 12px;
                        margin: 20px 0;
                    ">

                        <p>
                            <strong>اسم الفعالية:</strong>
                            {instance.title}
                        </p>

                        <p>
                            <strong>التاريخ:</strong>
                            {instance.date}
                        </p>

                        <p>
                            <strong>الموقع:</strong>
                            {instance.location}
                        </p>

                        <p>
                            <strong>السعر:</strong>
                            {instance.price}
                        </p>

                    </div>

                    <p>
                        شكرًا لاستخدامك منصة
                        <strong>EventHub</strong>.
                    </p>

                </div>

            </body>
            </html>
            """

            # -------------------------------------------------
            # إنشاء الرسالة
            # -------------------------------------------------

            email = EmailMultiAlternatives(
                subject="تمت إضافة الفعالية بنجاح - EventHub",

                body=text_content,

                from_email=None,

                to=[
                    instance.created_by.email
                ],
            )

            # إضافة نسخة HTML
            email.attach_alternative(
                html_content,
                "text/html"
            )

            # إرسال البريد
            email.send(
                fail_silently=False
            )

        # -----------------------------------------------------
        # التنفيذ بعد نجاح الـ transaction
        # -----------------------------------------------------

        transaction.on_commit(
            send_event_email
        )

