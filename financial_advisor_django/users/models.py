from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings

auth_user = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(
        auth_user,
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

    def __str__(self):
        return self.user.username
