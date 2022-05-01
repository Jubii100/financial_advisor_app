from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCreateAPI.as_view(), name='API_create_user'),
    path('profile/',
         views.UserProfileUpdateAPI.as_view(), name='API_user_profile_update'),
    path('budget/', views.UserBudgetAPI.as_view(), name='API_user_budget'),
    path('admin/', views.UserAdminAPI.as_view(), name='API_user_admin'),

]
