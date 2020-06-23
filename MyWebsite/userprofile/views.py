from django.contrib.auth import authenticate, login, logout
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from userprofile.forms import UserLoginForm, UserRegisterForm


# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验帐号密码是否匹配数据库中的某个用户
            # 如果均匹配则返回这个user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在session中，即实现了登陆操作
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse('帐号或密码输入错误，请重新输入！')
        else:
            # return HttpResponse('error:{} 帐号或密码输入不合法'.format(user_login_form.errors))
            return HttpResponse('帐号或密码输入不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {
            'form': user_login_form,
        }
        # print(context)
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请使用GET/POST请求数据')


# 用户退出
def uesr_logout(request):
    logout(request)
    return redirect('article:article_list')


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客界面
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误，请重新输入！！！')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {
            'form': user_register_form,
        }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET/POST方式访问')

# 删除用户（后续修改为逻辑删除）
# @login_required是一个装饰器。装饰器可以在不改变函数内容的前提下，给这个函数添加一些功能
# @login_required要求调用user_delete函数时，用户必须登录；
# 如果未登录则不执行函数，将页面重定向到login_url的地址
@login_required(login_url='userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登陆用户、待删除用户是否相同
        if request.user == user:
            # 退出登录，删除数据并返回博客列表
            # 日后进行修改，变成逻辑删除
            logout(request)
            user.delete()
            return redirect('article:article_list')
        else:
            return HttpResponse('你没有删除操作的权限')
    else:
        return HttpResponse('仅接受POST请求')
