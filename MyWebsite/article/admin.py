from django.contrib import admin

# Register your models here.
# 注册ArticlePost到admin中
from article.models import ArticlePost

admin.site.register(ArticlePost)
