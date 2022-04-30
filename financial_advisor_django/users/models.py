from django.dispatch import receiver
from django.db.models.signals import post_save
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
        models.CharField(max_length=128, null=True),
        size=5, null=True,
    )
    hobbies = ArrayField(
        models.CharField(max_length=128, null=True),
        size=5, null=True,
    )
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    net_worth = models.FloatField()

    def __str__(self):
        return self.user.username
