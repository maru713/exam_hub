"""
This module contains custom markdown settings for django-markdownx.
Provides a custom markdownify function with additional extensions.
"""
from django import template
from markdownx.utils import markdownify  # django-markdownx が提供する関数
from django.utils.safestring import mark_safe as safe

register = template.Library()

@register.filter(name='markdownx')
def markdownx_filter(value):
    """
    Markdown 記法のテキストを HTML に変換するフィルター
    """
    return safe(markdownify(value))
