from django.urls import path
from . import views

urlpatterns = [
    path('', views.career_list, name='career_list'),
    path('<int:pk>/', views.career_detail, name='career_detail'),
    path('<int:pk>/save/', views.toggle_save_career, name='toggle_save_career'),
    path('<int:pk>/review/', views.submit_review, name='submit_review'),
    path('review/<int:review_id>/vote/', views.vote_review, name='vote_review'),
    path('compare/', views.compare_careers, name='compare_careers'),
]
