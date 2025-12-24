from django.db import models
from django.conf import settings

class Assessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessments')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result_trait = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.started_at.strftime('%Y-%m-%d')}"

class Question(models.Model):
    class Type(models.TextChoices):
        INTEREST = 'INTEREST', 'Interest'
        SKILL = 'SKILL', 'Skill Perception'
        SCENARIO = 'SCENARIO', 'Scenario'
        
    class Trait(models.TextChoices):
        ANALYTICAL = 'ANALYTICAL', 'Analytical Thinking'
        CREATIVE = 'CREATIVE', 'Creative Expression'
        SOCIAL = 'SOCIAL', 'Social Engagement'
        TECHNICAL = 'TECHNICAL', 'Technical Aptitude'
        STRUCTURED = 'STRUCTURED', 'Structured Execution'

    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=Type.choices, default=Type.INTEREST)
    
    # Primary trait this question measures (for Interest/Skill types)
    primary_trait = models.CharField(max_length=20, choices=Trait.choices, blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.question_type}: {self.text[:50]}"
    
    class Meta:
        ordering = ['order']

class AnswerOption(models.Model):
    """Only for SCENARIO questions where users pick one option that maps to a trait."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    trait_associated = models.CharField(max_length=20, choices=Question.Trait.choices)
    
    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # For Interest/Skill (1-5 scale)
    value_score = models.IntegerField(null=True, blank=True, help_text="1-5 score")
    
    # For Scenario (Choice)
    selected_option = models.ForeignKey(AnswerOption, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assessment', 'question')
