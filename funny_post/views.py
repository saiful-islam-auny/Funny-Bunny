# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JokeForm, CommentForm
from .models import Joke, Category, Comment

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Joke, Like, Rating, Comment, SharedJoke
from .forms import JokeForm, CommentForm, RatingForm
from django.db import models
# Display jokes with filtering and search functionality
# views.py
def home(request, category_slug=None):
    query = request.GET.get('keyword')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        jokes = Joke.objects.filter(category=category)
    else:
        jokes = Joke.objects.all()

    if query:
        jokes = jokes.filter(title__icontains=query) | Joke.objects.filter(content__icontains=query)

    joke_like_counts = {joke.id: Like.objects.filter(joke=joke).count() for joke in jokes}
    joke_share_counts = {joke.id: SharedJoke.objects.filter(joke=joke).count() for joke in jokes}
    joke_ratings = {joke.id: Rating.objects.filter(joke=joke).aggregate(avg_rating=models.Avg('stars'))['avg_rating'] or 0 for joke in jokes}
    
    rating_forms = {joke.id: RatingForm() for joke in jokes}
    comment_forms = {joke.id: CommentForm() for joke in jokes}

    return render(request, 'index.html', {
        'jokes': jokes,
        'categories': Category.objects.all(),
        'joke_like_counts': joke_like_counts,
        'joke_share_counts': joke_share_counts,
        'joke_ratings': joke_ratings,
        'rating_forms': rating_forms,
        'comment_forms': comment_forms,
    })




# Submit a new joke
@login_required
def submit_joke(request):
    if request.method == 'POST':
        form = JokeForm(request.POST)
        if form.is_valid():
            joke = form.save(commit=False)
            joke.user = request.user
            joke.save()
            return redirect('home')
    else:
        form = JokeForm()
    return render(request, 'submit_joke.html', {'form': form})

# Edit an existing joke
@login_required
def edit_joke(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id, user=request.user)
    if request.method == 'POST':
        form = JokeForm(request.POST, instance=joke)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JokeForm(instance=joke)
    return render(request, 'accounts/user_profile.html', {'form': form})

# Delete a joke
@login_required
def delete_joke(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id, user=request.user)
    if request.method == 'POST':
        joke.delete()
        return redirect('home')
    return render(request, 'accounts/user_profile.html', {'joke': joke})

# Like a joke
@login_required
def like_joke(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id)
    like, created = Like.objects.get_or_create(user=request.user, joke=joke)
    if not created:
        like.delete()
    return redirect('home')

# Share a joke
@login_required
def share_joke(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id)
    if SharedJoke.objects.filter(user=request.user, joke=joke).exists():
        return HttpResponse('You have already shared this joke.', status=400)
    SharedJoke.objects.create(user=request.user, joke=joke)
    return redirect('profile')

# Add a comment to a joke
@login_required
def add_comment(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.joke = joke
            comment.save()
    return redirect('home')
# Add a rating to a joke
@login_required
def add_rating(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(user=request.user, joke=joke)
            rating.stars = form.cleaned_data['stars']
            rating.save()
    return redirect('home')

# User profile view to display jokes submitted and shared by the user
@login_required
def user_profile(request):
    submitted_jokes = Joke.objects.filter(user=request.user)
    shared_jokes = SharedJoke.objects.filter(user=request.user)
    
    # Initialize empty form
    joke_form = JokeForm()
    
    # Handle form submission for editing a joke
    if request.method == 'POST' and 'edit_joke_id' in request.POST:
        joke_id = request.POST.get('edit_joke_id')
        joke = get_object_or_404(Joke, id=joke_id)
        form = JokeForm(request.POST, instance=joke)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    
    return render(request, 'accounts/user_profile.html', {
        'submitted_jokes': submitted_jokes,
        'shared_jokes': shared_jokes,
        'joke_form': joke_form
    })





from django.shortcuts import render
from django.db.models import Count, Avg
from .models import Joke, Like, SharedJoke, Comment, Rating

def leaderboard(request):
    jokes = Joke.objects.annotate(
        like_count=Count('likes'),
        share_count=Count('shared_jokes'),
        comment_count=Count('comments'),
        avg_rating=Avg('ratings__stars')
    ).order_by('-like_count')[:5]
    
    return render(request, 'leaderboard.html', {'jokes': jokes})

