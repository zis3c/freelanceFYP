from django import forms
from .models import CareerReview

class CareerReviewForm(forms.ModelForm):
    """Form for submitting career reviews."""
    
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating-input'}),
        label="Rating"
    )
    
    review_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm',
            'placeholder': 'Share your experience with this career path...'
        }),
        label="Your Review",
        min_length=20,
        help_text="Minimum 20 characters"
    )
    
    experience_level = forms.ChoiceField(
        choices=CareerReview.ExperienceLevel.choices,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm'
        }),
        label="Your Experience Level"
    )
    
    class Meta:
        model = CareerReview
        fields = ['rating', 'review_text', 'experience_level']
