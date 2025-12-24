from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserDemographicsForm, StudentInterestForm
from .models import StudentProfile, CustomUser
from assessment.models import Assessment
from django.db.models import Count

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'ADMIN')

@user_passes_test(is_admin)
def admin_dashboard(request):
    # 1. Total Users (Students)
    student_count = CustomUser.objects.filter(role='STUDENT').count()
    
    # 2. Total Completed Assessments
    completed_assessments = Assessment.objects.filter(completed_at__isnull=False)
    assessment_count = completed_assessments.count()
    
    # 3. Trait Distribution
    # Result: [{'result_trait': 'CREATIVE', 'count': 5}, ...]
    trait_dist = completed_assessments.values('result_trait').annotate(count=Count('result_trait')).order_by('-count')
    
    # Prepare data for Chart.js
    labels = []
    data = []
    for item in trait_dist:
        trait = item['result_trait']
        if trait: # filter out None if any
            labels.append(trait)
            data.append(item['count'])
            
    context = {
        'student_count': student_count,
        'assessment_count': assessment_count,
        'chart_labels': labels,
        'chart_data': data,
    }
    
    return render(request, 'users/admin_dashboard.html', context)

@login_required
def profile_setup(request):
    # Ensure profile exists
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserDemographicsForm(request.POST, instance=request.user)
        profile_form = StudentInterestForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserDemographicsForm(instance=request.user)
        profile_form = StudentInterestForm(instance=profile)
        
    return render(request, 'users/profile_setup_final.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
