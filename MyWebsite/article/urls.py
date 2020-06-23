from django.urls import path

from . import views

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),
    # 文章详情
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('article-create/', views.articled_create, name='article_create'),
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    # 安全删除文章
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
]
