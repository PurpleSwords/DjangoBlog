from django.contrib.auth.models import User
from django.db import models

# 博客文章数据模型
from django.urls import reverse
from django.utils import timezone


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    # 文章标题。model.CharField为字符串字段，用于保存较短的字符串，例如标题
    title = models.CharField(max_length=100)

    # 文章正文。大文本用TextField
    body = models.TextField()

    # 文章浏览量，默认从0开始,PositiveIntegerField表示正整数
    total_views = models.PositiveIntegerField(default=0)

    # 文章创建时间。default=timezone.now指定在其创建数据时默认写入当前时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。auto_now=True指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给model定义元数据
    class Meta:
        # ordering指定模型返回的数据的排列顺序
        # '-created' 表明数据以创建时间倒序排序
        ordering = ('-created',)
        # 修改数据库表名
        db_table = 'ArticleData'

    # 函数__str__定义当调用对象的str()方法时的返回值内容
    def __str__(self):
        # 返回文章标题
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        # reverse:url反转，动态生成url
        # kwargs可以传递字典形式的参数
        return reverse('article:article_detail', args=[self.id])
