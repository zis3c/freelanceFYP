from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Industry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Career(models.Model):
    title = models.CharField(max_length=200)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='careers')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    
    skills = models.ManyToManyField(Skill, related_name='careers')
    education_required = models.CharField(max_length=200, help_text="Minimum education level required")
    salary_range = models.CharField(max_length=100, help_text="e.g. RM 2800 - RM 4500")
    outlook = models.TextField(help_text="Job market outlook description")
    
    class Trait(models.TextChoices):
        ANALYTICAL = 'ANALYTICAL', 'Analytical Thinking'
        CREATIVE = 'CREATIVE', 'Creative Expression'
        SOCIAL = 'SOCIAL', 'Social Engagement'
        TECHNICAL = 'TECHNICAL', 'Technical Aptitude'
        STRUCTURED = 'STRUCTURED', 'Structured Execution'

    primary_trait = models.CharField(
        max_length=20, 
        choices=Trait.choices, 
        blank=True, 
        null=True,
        help_text="The primary personality trait this career appeals to"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class SavedCareer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_careers')
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'career')
        ordering = ['-saved_at']

class CareerReview(models.Model):
    """User reviews for careers with ratings and written feedback."""
    
    class ExperienceLevel(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        ENTRY = 'ENTRY', 'Entry-level Professional'
        MID = 'MID', 'Mid-career Professional'
        SENIOR = 'SENIOR', 'Senior Professional'
    
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='career_reviews')
    
    rating = models.IntegerField(
        help_text="Rating from 1-5 stars",
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    review_text = models.TextField(help_text="Your detailed review")
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.STUDENT
    )
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'career')  # One review per user per career
    
    def __str__(self):
        return f"{self.user.username} - {self.career.title} ({self.rating}★)"
    
    @property
    def helpful_count(self):
        """Count of helpful votes."""
        return self.votes.filter(vote_type='HELPFUL').count()
    
    @property
    def not_helpful_count(self):
        """Count of not helpful votes."""
        return self.votes.filter(vote_type='NOT_HELPFUL').count()

class ReviewVote(models.Model):
    """Helpfulness votes on career reviews."""
    
    class VoteType(models.TextChoices):
        HELPFUL = 'HELPFUL', 'Helpful'
        NOT_HELPFUL = 'NOT_HELPFUL', 'Not Helpful'
    
    review = models.ForeignKey(CareerReview, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_votes')
    vote_type = models.CharField(max_length=20, choices=VoteType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'review')  # One vote per user per review
    
    def __str__(self):
        return f"{self.user.username} - {self.vote_type} on {self.review}"

