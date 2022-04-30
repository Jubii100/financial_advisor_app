from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserCreateAPI.as_view(), name='API_create_user'),
    path('user/profile/',
         views.UserProfileUpdateAPI.as_view(), name='API_user_profile_update'),

]
