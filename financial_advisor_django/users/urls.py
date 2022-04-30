from django.urls import path
from . import views

urlpatterns = [
    path('use-profile/',
         views.UserProfileDetailView.as_view(), name='user_profile'),
    path('user-profile-update/', views.UserProfileUpdateView.as_view(),
         name='user_profile_update'),
    # path('user_profile_create/',),
    path('create-users/', views.UserCreateView.as_view(), name='create_user'),
    # path('test', views.test, name='test'),
    path('API-create-user/', views.UserCreateAPI.as_view(), name='API_create_user'),
    path('API-user-profile-update/',
         views.UserProfileUpdateAPI.as_view(), name='API_user_profile_update'),

]
