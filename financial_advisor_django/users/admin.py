from django.contrib import admin
from .models import UserProfile, UserBudget

admin.site.register(UserProfile)
admin.site.register(UserBudget)
