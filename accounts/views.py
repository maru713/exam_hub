

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

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
