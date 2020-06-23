# 登录表单，继承了forms.Form类
from django import forms


# 用户登录
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    # 复写User的密码
    password = forms.CharField()
    password2 = forms.CharField()

    # 覆写某字段之后，内部类class Meta中的定义对这个字段就没有效果了，所以fields不用包含password
    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    # def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
    def clean_password2(self):
        data = self.cleaned_data
        # 从POST中取值data.get('password')和data['password']区别
        # 前者即使为空也不会导致程序错误，后者为空时如果data中不包含password会报错
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重试！')