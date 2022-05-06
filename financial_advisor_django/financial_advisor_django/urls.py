from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('user/', include(('users.urls', 'users'), namespace='user')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
