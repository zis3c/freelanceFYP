from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_home, name='assessment_home'),
    path('setup/', views.assessment_setup, name='assessment_setup'),
    path('take/', views.take_assessment, name='take_assessment'),
    path('save/<int:question_id>/', views.save_answer, name='save_answer'),
    path('results/', views.assessment_results, name='assessment_results'),
    path('retake/', views.retake_assessment, name='retake_assessment'),
    path('download-report/', views.download_report, name='download_report'),
]
