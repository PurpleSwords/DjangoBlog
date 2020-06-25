from django.contrib.auth.models import User
from django.db import models

# 用户扩展信息
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # 与Users模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


'''
在后台中创建并保存User时调用了信号接收函数，创建了Profile表；
但如果此时管理员填写了内联的Profile表，会导致此表也会被创建并保存。
最终结果就是同时创建了两个具有相同User的Profile表，违背了”一对一“外键的原则。
# 信号接收函数，每当更新User实例时自动调用
# post_save是一个内置信号，可以在模型调用save()方法后发出信号
# 信号接收函数，每当新建User实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''
