from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    
    # Core Apps
    path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('careers/', include('careers.urls')),
    path('assessment/', include('assessment.urls')),
    path('dashboard/', include('dashboard.urls')),
]
