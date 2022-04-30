from django.urls import path
from . import views

urlpatterns = [
    path('profile/view/',
         views.UserProfileDetailView.as_view(), name='user_profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(),
         name='user_profile_update'),
    path('', views.UserCreateView.as_view(), name='create_user'),

]
