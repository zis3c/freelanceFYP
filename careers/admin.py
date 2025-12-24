from django.contrib import admin
from .models import Industry, Career, Skill, SavedCareer, CareerReview, ReviewVote

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['title', 'industry', 'primary_trait', 'education_required']
    list_filter = ['industry', 'primary_trait']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['skills']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(SavedCareer)
class SavedCareerAdmin(admin.ModelAdmin):
    list_display = ['user', 'career', 'saved_at']
    list_filter = ['saved_at']

@admin.register(CareerReview)
class CareerReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'career', 'rating', 'experience_level', 'is_approved', 'created_at')
    list_filter = ('rating', 'experience_level', 'is_approved', 'is_flagged', 'created_at')
    search_fields = ('career__title', 'user__username', 'review_text')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_approved',)

@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('user__username', 'review__career__title')
