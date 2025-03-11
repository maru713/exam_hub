"""
This module contains form definitions for the Problem model, including Markdown support.
"""

from django import forms
from markdownx.widgets import MarkdownxWidget  # third-party import を上に移動
from .models import Problem

class ProblemForm(forms.ModelForm):
    """Form for creating and editing Problem instances with Markdown support."""

    class Meta:
        """Meta class defining model and fields for the Problem form."""

        model = Problem
        fields = ['title', 'body', 'answer', 'explanation', 'difficulty', 'category']
        widgets = {
            'body': MarkdownxWidget(),
            'answer': MarkdownxWidget(),
            'explanation': MarkdownxWidget(),
        }
