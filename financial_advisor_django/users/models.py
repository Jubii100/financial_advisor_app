from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class User_profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=128)
    interests = ArrayField(
        models.CharField(max_length=128, blank=True),
        size=5,
    )
    hobbies = ArrayField(
        models.CharField(max_length=128, blank=True),
        size=5,
    )
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    net_worth = models.FloatField()
