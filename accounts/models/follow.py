from django.conf import settings
from django.db import models
from .user import User  # 直接インポート
class Follow(models.Model):
    """
    Model representing a following relationship between users.
    'follower' follows 'following'.
    """
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following_set',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers_set',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        constraints = [
            models.CheckConstraint(check=~models.Q(follower=models.F('following')), name='prevent_self_follow')
        ]

    def __str__(self):
        return f"{self.follower} follows {self.following}"