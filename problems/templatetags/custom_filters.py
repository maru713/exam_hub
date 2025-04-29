from django import template

register = template.Library()

@register.filter
def get_by_key(dictionary, key):
    return dictionary.get(key)

@register.filter
def dict_get(d, key):
    """テンプレート内で辞書からキーで値を取得するフィルタ"""
    return d.get(key)