from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCreateAPI.as_view(), name='API_create_user'),
    path('login/', views.LoginAPI.as_view(), name='Login_API'),
    path('logout/', views.LogOutAPI.as_view(), name='Logout_API'),
    path('profile/',
         views.UserProfileUpdateAPI.as_view(), name='API_user_profile_update'),
    path('budget/', views.UserBudgetAPI.as_view(), name='API_user_budget'),
    path('financial_data/<str:mk>/<int:sk>/<int:ek>/',
         views.TopTenUsersAPI.as_view(), name='API_users_range'),
    path('financial_data/<str:mk>/<int:sk>/',
         views.TopTenUsersAPI.as_view(), name='API_users_range'),
    path('financial_data/<str:mk>/',
         views.TopTenUsersAPI.as_view(), name='API_top10_users'),
    path('external/', views.ExternalAPI.as_view(), name='external_API'),
]
