from django import forms
from .models import CustomUser, StudentProfile

class UserDemographicsForm(forms.ModelForm):
    AGE_CHOICES = [
        ('', 'Select Age Range'),
        ('13-15', '13-15 years old'),
        ('16-17', '16-17 years old'),
        ('18-20', '18-20 years old'),
        ('21+', '21+ years old'),
    ]
    
    EDU_CHOICES = [
        ('', 'Select Education Level'),
        ('Form 3', 'Form 3'),
        ('Form 4', 'Form 4'),
        ('Form 5', 'Form 5 (SPM)'),
        ('Pre-U', 'Pre-University / Diploma'),
    ]

    age_range = forms.ChoiceField(choices=AGE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    education_level = forms.ChoiceField(choices=EDU_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. Kuala Lumpur'}))
    gender = forms.ChoiceField(choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')], required=True)
    
    class Meta:
        model = CustomUser
        fields = ['age_range', 'education_level', 'location', 'gender']

class StudentInterestForm(forms.ModelForm):
    INTEREST_CHOICES = [
        ('STEM', 'Science & Technology'),
        ('ARTS', 'Arts & Design'),
        ('BUSINESS', 'Business & Entrepreneurship'),
        ('HUMANITIES', 'Social Sciences & Humanities'),
        ('SPORTS', 'Sports & Athletics'),
    ]

    # Map JSONField to a MultipleChoiceField
    academic_interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Please select at least one interest.'}
    )

    class Meta:
        model = StudentProfile
        fields = ['academic_interests', 'has_career_in_mind', 'target_career', 'confidence_level']
        widgets = {
            'target_career': forms.TextInput(attrs={'placeholder': 'e.g. Software Engineer (Optional)'}),
            'confidence_level': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5', 'step': '1'}),
        }
