from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
import markdown

from article.forms import ArticlePostForm
from article.models import ArticlePost


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')

    if search:
        # 根据GET请求中的查询条件，返回不同排序的对象数组
        if order == 'total_views':
            article_lists = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)) \
                .order_by('-total_views')
        else:
            # 取出所有博客文章(默认排序)
            article_lists = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    else:
        # 将search参数置空
        search = ''
        if order == 'total_views':
            article_lists = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_lists = ArticlePost.objects.all()
    # 每页显示3篇文章
    paginator = Paginator(article_lists, 3)
    # 获取url中的页码(通过GET的键值对参数请求:?key=value)
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给article
    articles = paginator.get_page(page)
    # 需要传递给模板的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
    }
    return render(request, 'article/list.html', context=context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)

    # 浏览量+1
    article.total_views += 1
    # 保存使用参数，只更新指定字段。
    # 不带参数的话，会更新全部字段，包括更新时间字段（导致该字段内容错误）
    article.save(update_fields=['total_views'])
    # article.save()
    print(article.updated)
    # 将markdown语法渲染成html样式
    # 欠缺：代码没有行号
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展(需要加入标记[TOC])
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 需要传递给模板的对象
    context = {
        'article': article,
        'toc': md.toc
    }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 写文章的视图
# 检查登录
@login_required(login_url='/userprofile/login/')
def articled_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定作者为当前登录用户
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存在数据库中
            new_article.save()
            # 完成后返回文章列表
            return redirect('article:article_list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写！！！')

    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {
            'article_post_form': article_post_form,
        }
        return render(request, 'article/create.html', context)


# 删文章，需要对用户进行身份验证（未进行）
@login_required(login_url='/userprofile/login')
def article_delete(request, id):
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用delete方法删除文章
    article.delete()
    return redirect('article:article_list')


# 安全删除文章（只允许POST请求），需要对用户进行身份验证（未进行）
@login_required(login_url='/userprofile/login')
def article_safe_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    # 过滤非法用户
    if request.user != article.author:
        return HttpResponse('很抱歉，您无权删除本文章')
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('非法请求！')


# 更新文章
@login_required(login_url='/userprofile/login')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新title、body字段
    GET方法进入初始表单页面
    :param request:
    :param id: 文章的id
    :return:
    """
    # 获取需要修改的具体文章的对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非法用户
    if request.user != article.author:
        return HttpResponse('很抱歉，您无权修改本文章')
    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        '''
        另一种方法：
        article_post_form = ArticlePostForm(data=request.POST, instance=article)
        if article_post_form.is_valid():
            article_post_form.save()
        '''
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的title、body数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改的文章中，需传入文章的id值
            return redirect('article:article_detail', id=id)
        # 数据不合法，返回错误信息
        else:
            return HttpResponse('表单信息有误，请重新填写')

    # 如果用户GET请求获取数据
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将article文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
        }
        return render(request, 'article/update.html', context)
