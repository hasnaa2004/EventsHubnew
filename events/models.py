
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    # ==============================
    # حالات الفعاليات
    # ==============================

    STATUS_CHOICES = [
        ('available', 'متاح'),
        ('full', 'مكتمل'),
        ('cancelled', 'ملغي'),
    ]

    # ==============================
    # تصنيفات الفعاليات
    # ==============================

    CATEGORY_CHOICES = [
        ('course', 'دورة'),
        ('workshop', 'ورشة'),
        ('conference', 'مؤتمر'),
        ('seminar', 'ندوة'),
    ]

    # ==============================
    # أنواع الفعاليات
    # ==============================

    TYPE_CHOICES = [
        ('onsite', 'حضوري'),
        ('online', 'أونلاين'),
        ('hybrid', 'مختلط'),
    ]

    # ==============================
    # المدن
    # ==============================

    CITY_CHOICES = [
        ('sanaa', 'صنعاء'),
        ('aden', 'عدن'),
        ('taiz', 'تعز'),
        ('ibb', 'إب'),
        ('hodeidah', 'الحديدة'),
        ('hadramout', 'حضرموت'),
    ]

    # ==============================
    # بيانات الفعالية
    # ==============================

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    date = models.DateTimeField()

    location = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='course'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    event_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='onsite'
    )

    city = models.CharField(
        max_length=30,
        choices=CITY_CHOICES,
        default='sanaa'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # ==============================
    # صورة الفعالية
    # ==============================

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True
    )

    # ==============================
    # المستخدم الذي أنشأ الفعالية
    # ==============================

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events',
        null=True,
        blank=True
    )

    # ==============================
    # عرض اسم الفعالية
    # ==============================

    def __str__(self):
        return self.title

class Notification(models.Model):

    # المستخدم الذي سيستلم الإشعار
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # نص الإشعار
    message = models.TextField()

    # هل قرأ المستخدم الإشعار؟
    is_read = models.BooleanField(
        default=False
    )

    # وقت إنشاء الإشعار
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.recipient.username} - {self.message[:40]}"