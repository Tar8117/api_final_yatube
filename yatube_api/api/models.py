from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, F

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Имя группы', max_length=200)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name='group', blank=True,
        null=True, db_index=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings'
    )

    # может так?
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            ),
            CheckConstraint(
                check=~Q(user=F('following')), name='self_follow_ban'
            )
        ]
