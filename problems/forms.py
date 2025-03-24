"""
This module contains form definitions for the Problem model, including Markdown support.
"""

from django import forms
from markdownx.widgets import MarkdownxWidget  # third-party import を上に移動
from .models import Problem, Answer
class ProblemForm(forms.ModelForm):
    """Form for creating and editing Problem instances with Markdown support."""
    class Meta:
        """Meta class defining model and fields for the Problem form."""
        model = Problem
        fields = ['title', 'body', 'answer', 'explanation', 'difficulty', 'grade', 'subject', 'topic', 'tags']

        widgets = {
            'body': MarkdownxWidget(),
            'answer': MarkdownxWidget(),
            'explanation': MarkdownxWidget(),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Markdownで回答を記述してください'}),
        }