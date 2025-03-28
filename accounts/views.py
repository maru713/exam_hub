from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Follow, User
from problems.models import Problem, Answer, AnswerReaction

def login_view(request):
    """
    Handles user login.

    If the request method is POST, it attempts to authenticate the user.
    If authentication is successful, the user is logged in and redirected to the problems list.
    Otherwise, it renders the login form again with an error message.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('problems:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    Handles user logout.

    Logs out the current user and redirects them to the problems list page.
    """
    logout(request)
    return redirect('problems:list')

def register_view(request):
    """Handles user registration. Displays the registration form and processes user input."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

User = get_user_model()

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'profile_user': user,
        'is_own_profile': request.user == user,
        'followers_count': Follow.objects.filter(following=user).count(),
        'following_count': Follow.objects.filter(follower=user).count(),
        'user_problems': Problem.objects.filter(author=user),
    }
    return render(request, 'accounts/profile.html', context=context)

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        Follow.objects.get_or_create(follower=request.user, following=target_user)
    return redirect('accounts:profile', username=username)

@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=target_user).delete()
    return redirect('accounts:profile', username=username)

@login_required
def mypage_view(request):
    user = request.user
    context = {
        'profile_user': user,
        'is_own_profile': True,
        'followers_count': Follow.objects.filter(following=user).count(),
        'following_count': Follow.objects.filter(follower=user).count(),
        'user_problems': Problem.objects.filter(author=user),
    }
    return render(request, 'accounts/mypage.html', context)

@login_required
def toggle_reaction(request, answer_id, reaction_type):
    """
    ユーザーが回答に👍👎リアクションするビュー
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    reaction, created = AnswerReaction.objects.get_or_create(
        user=request.user,
        answer=answer,
        defaults={'is_good': reaction_type == 'good'}
    )

    if not created:
        if reaction.reaction_type == reaction_type:
            reaction.delete()  # 同じ反応を2回押すと取り消し
        else:
            reaction.reaction_type = reaction_type
            reaction.save()

    return redirect('problem_detail', pk=answer.problem.id)