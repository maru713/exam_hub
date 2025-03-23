# accounts/templatetags/follow_tags.py
from django import template
from accounts.models import Follow

register = template.Library()
# accounts/templatetags/follow_tags.py

@register.filter
def is_following(user, other_user):
    if user.is_authenticated:
        return Follow.objects.filter(follower=user, following=other_user).exists()
    return False