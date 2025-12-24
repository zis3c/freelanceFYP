from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from .models import Career, SavedCareer, Industry, CareerReview, ReviewVote
from .forms import CareerReviewForm
from assessment.models import Assessment

def career_list(request):
    query = request.GET.get('q', '')
    industry_id = request.GET.get('industry', '')
    
    careers = Career.objects.all()
    
    if query:
        careers = careers.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if industry_id:
        careers = careers.filter(industry__id=industry_id)
        
    industries = Industry.objects.all()
    
    context = {
        'careers': careers,
        'industries': industries,
        'query': query,
        'selected_industry': int(industry_id) if industry_id else None
    }
    return render(request, 'careers/career_list.html', context)

def career_detail(request, pk):
    career = get_object_or_404(Career, pk=pk)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedCareer.objects.filter(user=request.user, career=career).exists()
    
    # Get reviews with filtering
    reviews = CareerReview.objects.filter(career=career, is_approved=True)
    filter_by = request.GET.get('filter', 'recent')
    
    if filter_by == 'highest':
        reviews = reviews.order_by('-rating', '-created_at')
    elif filter_by == 'helpful':
        reviews = reviews.annotate(
            helpful_votes=Count('votes', filter=Q(votes__vote_type='HELPFUL'))
        ).order_by('-helpful_votes', '-created_at')
    else:  # 'recent' is default
        reviews = reviews.order_by('-created_at')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    # Rating distribution
    rating_dist = {i: reviews.filter(rating=i).count() for i in range(1, 6)}
    
    # Check if user has already reviewed
    user_review = None
    if request.user.is_authenticated:
        user_review = CareerReview.objects.filter(user=request.user, career=career).first()
    
    # Get user's votes on reviews
    user_helpful_votes = set()
    user_not_helpful_votes = set()
    if request.user.is_authenticated:
        votes = ReviewVote.objects.filter(user=request.user, review__in=reviews)
        for vote in votes:
            if vote.vote_type == 'HELPFUL':
                user_helpful_votes.add(vote.review_id)
            else:
                user_not_helpful_votes.add(vote.review_id)
    
    # Get user's latest assessment trait for compatibility check
    user_trait = None
    if request.user.is_authenticated:
        latest_assessment = Assessment.objects.filter(user=request.user, completed_at__isnull=False).order_by('-completed_at').first()
        if latest_assessment:
            user_trait = latest_assessment.result_trait

    # Review form
    review_form = CareerReviewForm() if request.user.is_authenticated and not user_review else None
    
    return render(request, 'careers/career_detail.html', {
        'career': career, 
        'is_saved': is_saved,
        'reviews': reviews,
        'review_form': review_form,
        'avg_rating': avg_rating,
        'rating_dist': rating_dist,
        'total_reviews': reviews.count(),
        'filter_by': filter_by,
        'user_review': user_review,
        'user_helpful_votes': user_helpful_votes,
        'user_not_helpful_votes': user_not_helpful_votes,
        'user_trait': user_trait,
    })

@login_required
def compare_careers(request):
    c1_id = request.GET.get('c1')
    c2_id = request.GET.get('c2')
    
    context = {}
    if c1_id and c2_id:
        c1 = get_object_or_404(Career, pk=c1_id)
        c2 = get_object_or_404(Career, pk=c2_id)
        context['c1'] = c1
        context['c2'] = c2
        
    return render(request, 'careers/compare_v2.html', context)

@login_required
def toggle_save_career(request, pk):
    career = get_object_or_404(Career, pk=pk)
    saved_item = SavedCareer.objects.filter(user=request.user, career=career).first()
    
    if saved_item:
        saved_item.delete()
    else:
        SavedCareer.objects.create(user=request.user, career=career)
        
    return redirect('career_detail', pk=pk)

@login_required
def submit_review(request, pk):
    """Handle review submission for a career."""
    career = get_object_or_404(Career, pk=pk)
    
    # Check if user already reviewed this career
    existing_review = CareerReview.objects.filter(user=request.user, career=career).first()
    if existing_review:
        return redirect('career_detail', pk=pk)
    
    if request.method == 'POST':
        form = CareerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.career = career
            review.save()
            return redirect('career_detail', pk=pk)
    
    return redirect('career_detail', pk=pk)

@login_required
def vote_review(request, review_id):
    """Handle voting on review helpfulness (AJAX endpoint)."""
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    review = get_object_or_404(CareerReview, pk=review_id)
    
    # Prevent voting on own review
    if review.user == request.user:
        return JsonResponse({'error': 'Cannot vote on your own review'}, status=403)
    
    vote_type = request.POST.get('vote_type')
    if vote_type not in ['HELPFUL', 'NOT_HELPFUL']:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)
    
    # Check existing vote
    existing_vote = ReviewVote.objects.filter(user=request.user, review=review).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote if clicking same button
            existing_vote.delete()
            action = 'removed'
        else:
            # Change vote type
            existing_vote.vote_type = vote_type
            existing_vote.save()
            action = 'changed'
    else:
        # Create new vote
        ReviewVote.objects.create(user=request.user, review=review, vote_type=vote_type)
        action = 'added'
    
    return JsonResponse({
        'success': True,
        'action': action,
        'helpful_count': review.helpful_count,
        'not_helpful_count': review.not_helpful_count,
    })

