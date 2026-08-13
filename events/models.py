from django.db import models


class Event(models.Model):

    STATUS_CHOICES = [
        ('available', 'متاح'),
        ('full', 'مكتمل'),
        ('cancelled', 'ملغي'),
    ]

    CATEGORY_CHOICES = [
        ('course', 'دورة'),
        ('workshop', 'ورشة'),
        ('conference', 'مؤتمر'),
        ('seminar', 'ندوة'),
    ]

    TYPE_CHOICES = [
        ('onsite', 'حضوري'),
        ('online', 'أونلاين'),
        ('hybrid', 'مختلط'),
    ]

    CITY_CHOICES = [
        ('sanaa', 'صنعاء'),
        ('aden', 'عدن'),
        ('taiz', 'تعز'),
        ('ibb', 'إب'),
        ('hodeidah', 'الحديدة'),
        ('hadramout', 'حضرموت'),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    date = models.DateTimeField()

    location = models.CharField(max_length=200)

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

    def __str__(self):
        return self.title