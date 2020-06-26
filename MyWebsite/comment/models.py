from django.contrib.auth.models import User
from django.db import models

from article.models import ArticlePost


# 博文评论
class Comment(models.Model):
    # related_name类似设置外键别名
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]
