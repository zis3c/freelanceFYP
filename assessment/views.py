from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Assessment, Question, UserAnswer

@login_required
def assessment_home(request):
    """Landing page for assessment."""
    return render(request, 'assessment/home.html')

@login_required
def assessment_setup(request):
    """Creates a new assessment or retrieves the latest incomplete one."""
    # Check for incomplete assessment
    assessment = Assessment.objects.filter(
        user=request.user, 
        completed_at__isnull=True
    ).last()
    
    if not assessment:
        assessment = Assessment.objects.create(user=request.user)
        
    return redirect('take_assessment')

@login_required
def take_assessment(request):
    """Displays the next unanswered question."""
    assessment = Assessment.objects.filter(
        user=request.user, 
        completed_at__isnull=True
    ).last()
    
    if not assessment:
        return redirect('assessment_home')

    # Find answered question IDs
    answered_ids = UserAnswer.objects.filter(assessment=assessment).values_list('question_id', flat=True)
    
    # Get next question
    question = Question.objects.exclude(id__in=answered_ids).filter(is_active=True).order_by('order').first()
    
    if not question:
        # No more questions, mark complete
        assessment.completed_at = timezone.now()
        assessment.save()
        return redirect('assessment_results')
    
    # Calculate progress
    total_questions = Question.objects.filter(is_active=True).count()
    answered_count = len(answered_ids)
    progress_percentage = (answered_count / total_questions) * 100 if total_questions > 0 else 0

    return render(request, 'assessment/question.html', {
        'question': question,
        'assessment': assessment,
        'progress': round(progress_percentage)
    })

@login_required
def save_answer(request, question_id):
    if request.method != 'POST':
        return redirect('take_assessment')

    assessment = Assessment.objects.filter(
        user=request.user, 
        completed_at__isnull=True
    ).last()
    
    if not assessment:
        return redirect('assessment_home')
        
    question = get_object_or_404(Question, id=question_id)
    
    # Save Logic based on type
    if question.question_type in [Question.Type.INTEREST, Question.Type.SKILL]:
        score = request.POST.get('score')
        if score:
            UserAnswer.objects.create(
                assessment=assessment,
                question=question,
                value_score=int(score)
            )
    # Add Scenario logic here later if needed
    
    return redirect('take_assessment')

@login_required
def assessment_results(request):
    assessment = Assessment.objects.filter(
        user=request.user, 
        completed_at__isnull=False
    ).last()
    
    if not assessment:
        return redirect('assessment_home')
        
    # Calculate Scores
    scores = {
        'ANALYTICAL': 0,
        'CREATIVE': 0,
        'SOCIAL': 0,
        'TECHNICAL': 0,
        'STRUCTURED': 0,
    }
    
    # Get all answers
    answers = UserAnswer.objects.filter(assessment=assessment).select_related('question')
    
    for answer in answers:
        if answer.question.primary_trait and answer.value_score:
            scores[answer.question.primary_trait] += answer.value_score
            
    # Determine Top Trait
    top_trait_code = max(scores, key=scores.get)
    top_trait_label = dict(Question.Trait.choices).get(top_trait_code, 'Unknown')
    
    # Save the result to the database if not already saved (Analytics)
    if not assessment.result_trait:
        assessment.result_trait = top_trait_code
        assessment.save(update_fields=['result_trait'])
    
    # Prepare Display Data (Score + Percentage)
    # Max score per trait = 10 (2 questions * 5 points)
    MAX_SCORE = 10
    trait_scores = []
    
    for trait_code, score in scores.items():
        label = dict(Question.Trait.choices).get(trait_code, trait_code)
        percentage = min((score / MAX_SCORE) * 100, 100) # Cap at 100
        trait_scores.append({
            'label': label,
            'score': score,
            'percentage': int(percentage)
        })
        
    # Sort for display (highest first)
    trait_scores.sort(key=lambda x: x['score'], reverse=True)

    # Matching Careers
    from careers.models import Career 
    recommended_careers = Career.objects.filter(primary_trait=top_trait_code)[:3]
    
    print(f"DEBUGGING VIEW: top_trait={top_trait_label}")
    context = {
        'assessment': assessment,
        'trait_scores': trait_scores,
        'dominant_trait': top_trait_label,
        'careers': recommended_careers,
        'debug_check': "SYSTEM_ACTIVE"
    }
    return render(request, 'assessment/results_v2.html', context)

@login_required
def retake_assessment(request):
    """Resets the user's unfinished assessment or creates a new one."""
    # Mark any existing incomplete assessments as abandoned (or just delete them)
    # Ideally, we might want to keep history but for now, simple restart:
    
    # 1. Create a NEW assessment
    Assessment.objects.create(user=request.user)
    
    # 2. Redirect to start
    return redirect('take_assessment')

@login_required
def download_report(request):
    """Generate and download PDF report of assessment results."""
    from django.http import HttpResponse
    from xhtml2pdf import pisa
    from django.template.loader import render_to_string
    
    assessment = Assessment.objects.filter(
        user=request.user, 
        completed_at__isnull=False
    ).last()
    
    if not assessment:
        return redirect('assessment_home')
        
    # Calculate Scores (same logic as results view)
    scores = {
        'ANALYTICAL': 0,
        'CREATIVE': 0,
        'SOCIAL': 0,
        'TECHNICAL': 0,
        'STRUCTURED': 0,
    }
    
    answers = UserAnswer.objects.filter(assessment=assessment).select_related('question')
    for answer in answers:
        if answer.question.primary_trait and answer.value_score:
            scores[answer.question.primary_trait] += answer.value_score
            
    top_trait_code = max(scores, key=scores.get)
    top_trait_label = dict(Question.Trait.choices).get(top_trait_code, 'Unknown')
    
    MAX_SCORE = 10
    trait_scores = []
    for trait_code, score in scores.items():
        label = dict(Question.Trait.choices).get(trait_code, trait_code)
        percentage = min((score / MAX_SCORE) * 100, 100)
        trait_scores.append({
            'label': label,
            'score': score,
            'percentage': int(percentage)
        })
    trait_scores.sort(key=lambda x: x['score'], reverse=True)

    from careers.models import Career 
    recommended_careers = Career.objects.filter(primary_trait=top_trait_code)[:3]
    
    context = {
        'user': request.user,
        'assessment': assessment,
        'trait_scores': trait_scores,
        'dominant_trait': top_trait_label,
        'careers': recommended_careers,
    }
    
    html = render_to_string('assessment/report_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="assessment_report_{request.user.username}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response
