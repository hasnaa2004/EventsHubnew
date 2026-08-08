from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name