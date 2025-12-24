from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', _('Student')
        ADMIN = 'ADMIN', _('Admin')
        COUNSELOR = 'COUNSELOR', _('Career Counselor')

    role = models.CharField(
        max_length=50, 
        choices=Role.choices, 
        default=Role.STUDENT,
        verbose_name=_('Role')
    )
    
    # Basic Demographics
    age_range = models.CharField(max_length=20, blank=True, null=True)
    education_level = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    
    # Interests stored as JSON list
    academic_interests = models.JSONField(default=list, blank=True) 
    
    # Career Awareness
    has_career_in_mind = models.BooleanField(default=False)
    target_career = models.CharField(max_length=200, blank=True, null=True)
    confidence_level = models.IntegerField(default=0, help_text="1-5 scale")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
