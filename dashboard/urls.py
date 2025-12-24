from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('saved/', views.saved_careers, name='saved_careers'),
]
