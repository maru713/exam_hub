"""
This module defines the data models for exam hub problems.
It contains classes and functions that manage problem data, validations,
and interactions with other parts of the application.
"""
from django.db import models
from django.conf import settings
from markdownx.models import MarkdownxField


class ProblemCategory(models.Model):
    """
    ProblemCategory represents a category for grouping problems.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)



class Problem(models.Model):
    """
    Problem represents a practice problem or question.

    Attributes:
        title (str): The title of the problem.
        body (str): The main content of the problem, supporting Markdown.
        answer (str): The answer to the problem.
        explanation (str): Optional explanation or commentary.
        difficulty (int): The difficulty level of the problem.
        category (ProblemCategory): The category to which the problem belongs.
        created_at (datetime): The timestamp when the problem was created.
    """
    title = models.CharField(max_length=200)
    # MarkdownxField に変更することで、Markdown の入力・保存が可能
    body = MarkdownxField()
    answer = MarkdownxField()  # 解答も Markdown にすると、リッチなフォーマットが可能
    explanation = MarkdownxField(blank=True, null=True)
    difficulty = models.IntegerField(default=1)
    category = models.ForeignKey(
        ProblemCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='problems'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

