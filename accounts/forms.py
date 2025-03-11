"""
This module contains form definitions for user authentication and problem creation.
"""

from django.contrib.auth.forms import UserCreationForm
from .models import User  # カスタムユーザーの場合

class UserRegisterForm(UserCreationForm):  # pylint: disable=too-few-public-methods
    """Form for user registration with username, email, and password validation."""

    class Meta:
        """Defines model and fields for User registration form."""

        model = User
        fields = ['username', 'email', 'password1', 'password2']
