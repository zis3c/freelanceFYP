from django.contrib import admin
from .models import Question, AnswerOption, Assessment, UserAnswer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question_type', 'primary_trait', 'order', 'is_active']
    list_filter = ['question_type', 'primary_trait', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['text']

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'trait_associated']
    list_filter = ['trait_associated']

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'started_at', 'completed_at', 'result_trait']
    list_filter = ['completed_at', 'result_trait']
    search_fields = ['user__username']
    readonly_fields = ['started_at']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'question', 'value_score', 'created_at']
    list_filter = ['created_at']
