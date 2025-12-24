from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from assessment.models import Assessment, UserAnswer, Question
from careers.models import SavedCareer

@login_required
def dashboard(request):
    # Check if profile is complete (e.g. basic demographics)
    # Using getattr to avoid crash if field doesn't exist yet in session/user
    if not getattr(request.user, 'age_range', None) or not getattr(request.user, 'location', None):
        return redirect('profile_setup')

    # Get latest assessment
    assessment = Assessment.objects.filter(user=request.user).last()
    
    assessment_status = "Not Started"
    top_trait = None
    
    if assessment:
        if assessment.completed_at:
            assessment_status = "Completed"
            
            # fast calculation for dashboard
            scores = {}
            answers = UserAnswer.objects.filter(assessment=assessment).select_related('question')
            for answer in answers:
                if answer.question.primary_trait and answer.value_score:
                    trait = answer.question.primary_trait
                    scores[trait] = scores.get(trait, 0) + answer.value_score
            
            if scores:
                top_trait_code = max(scores, key=scores.get)
                top_trait = dict(Question.Trait.choices).get(top_trait_code, top_trait_code)
        else:
            assessment_status = "In Progress"

    # Get saved careers count
    saved_count = SavedCareer.objects.filter(user=request.user).count()

    # Check profile status for display
    is_profile_complete = getattr(request.user, 'age_range', None) and getattr(request.user, 'location', None)

    return render(request, 'dashboard/dashboard.html', {
        'assessment': assessment,
        'assessment_status': assessment_status,
        'top_trait': top_trait,
        'saved_count': saved_count,
        'is_profile_complete': is_profile_complete
    })

@login_required
def saved_careers(request):
    saved = SavedCareer.objects.filter(user=request.user).select_related('career', 'career__industry')
    return render(request, 'dashboard/saved_careers.html', {'saved_careers': saved})
