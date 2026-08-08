from django.db import models

# Create your models here.
from django.db import models


class Event(models.Model):

    STATUS_CHOICES = [
        ('available', 'متاح'),
        ('cancelled', 'ملغي'),
    ]

    CATEGORY_CHOICES = [
        ('course', 'دورة'),
        ('workshop', 'ورشة'),
        ('conference', 'مؤتمر'),
        ('seminar', 'ندوة'),
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

    def __str__(self):
        return self.title