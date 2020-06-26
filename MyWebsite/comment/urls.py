from django.urls import path

from . import views

urlpatterns = [
    # 发表评论
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]
