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
        answer_text (Text): Markdown形式で記述された本文。
        explanation (Text): 任意の解説。
        created_at (DateTime): 作成日時。
        updated_at (DateTime): 更新日時。
    """
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    answer_text = MarkdownxField(help_text="ユーザーが考える解答")
    explanation = MarkdownxField(blank=True, null=True, help_text="解答の補足や解説（任意）")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer by {self.author} on {self.problem}"
    def good_count(self):
        return self.reactions.filter(is_good=True).count()

    def bad_count(self):
        return self.reactions.filter(is_good=False).count()
class AnswerReaction(models.Model):
    """ユーザーによる単一リアクション（Good / Bad）"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='reactions')
    is_good = models.BooleanField(default=True)
    reacted_at = models.DateTimeField(auto_now_add=True)  # 👍👎の日時

    class Meta:
        unique_together = ('user', 'answer')  # 二重リアクション防止

class AnswerRating(models.Model):
    """回答に対する3つの観点での評価（任意）"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='ratings')
    clarity = models.PositiveSmallIntegerField()     # 明瞭さ
    accuracy = models.PositiveSmallIntegerField()    # 正確さ
    originality = models.PositiveSmallIntegerField() # 独自性
    rated_at = models.DateTimeField(auto_now_add=True)  # 評価日時

    class Meta:
        unique_together = ('user', 'answer')  # 同一ユーザーの多重評価防止
