from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/',
         views.UserProfileDetailView.as_view(), name='user_profile'),
    path('user_profile_update/', views.UserProfileUpdateView.as_view(),
         name='user_profile_update'),
    # path('user_profile_create/',),
    path('create_users/', views.UserCreateView.as_view(), name='create_user'),
    #path('test', views.test, name='test'),
]
