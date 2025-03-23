"""
This module defines the data models for exam hub problems.
It contains classes and functions that manage problem data, validations,
and interactions with other parts of the application.
"""
from django.db import models
from django.conf import settings
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager  # タグ機能
class Grade(models.Model):
    """学年 (例: 中学1年、高校2年)"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    """教科 (例: 数学、英語、理科)"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    """単元 (例: 数学の「確率」、英語の「文法」)"""
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")

    class Meta:
        unique_together = ('name', 'subject')

    def __str__(self):
        return f"{self.subject.name} - {self.name}"



class Problem(models.Model):
    """
    Problem represents a practice problem or question.

    Attributes:
        title (str): The title of the problem.
        body (str): The main content of the problem, supporting Markdown.
        answer (str): The answer to the problem.
        explanation (str): Optional explanation or commentary.
        difficulty (int): The difficulty level of the problem.
        created_at (datetime): The timestamp when the problem was created.
    """
    title = models.CharField(max_length=200)
    # MarkdownxField に変更することで、Markdown の入力・保存が可能
    body = MarkdownxField()
    answer = MarkdownxField()  # 解答も Markdown にすると、リッチなフォーマットが可能
    explanation = MarkdownxField(blank=True, null=True)
    difficulty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True, related_name="problems")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="problems")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="problems")

    # タグ機能を追加
    tags = TaggableManager(blank=True)

    def __str__(self):
        return str(self.title)

class Answer(models.Model):
    """
    ユーザーが投稿した問題への回答。

    Attributes:
        problem (ForeignKey): 回答対象の問題。
        author (ForeignKey): 回答者。
        content (Text): Markdown形式で記述された本文。
        image (Image): 任意の画像（数式の手書きなど）。
        created_at (DateTime): 作成日時。
        updated_at (DateTime): 更新日時。
    """
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    content = MarkdownxField()
    image = models.ImageField(upload_to='answer_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer by {self.author} on {self.problem}"
