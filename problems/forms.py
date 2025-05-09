"""
This module contains form definitions for the Problem model, including Markdown support.
"""

from django import forms
from markdownx.widgets import MarkdownxWidget  # third-party import を上に移動
from .models import Problem, Answer, AnswerComment

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
        fields = ['answer_text', 'explanation', 'purposes']
        widgets = {
            'answer_text': forms.Textarea(attrs={'rows': 4}),
            'explanation': forms.Textarea(attrs={'rows': 3}),
            'purposes': forms.CheckboxSelectMultiple(),  # ← 複数選択を明示
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purposes'].required = True  # ← ここがキモ

class AnswerCommentForm(forms.ModelForm):
    class Meta:
        model = AnswerComment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'コメントを入力...'}),
        }