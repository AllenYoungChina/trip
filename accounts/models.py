from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import CommonModel


class User(AbstractUser):
    """ 用户模型 """
    avatar = models.ImageField(verbose_name='用户头像', upload_to='avatar/%Y%m', blank=True, null=True)
    nickname = models.CharField(verbose_name='用户昵称', max_length=32, unique=True)

    class Meta:
        db_table = 'account_user'
        verbose_name = '用户基础信息'
        verbose_name_plural = verbose_name

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else ''

    def add_login_record(self, **kwargs):
        """ 记录用户登录日志 """
        self.login_records.create(**kwargs)


class Profile(models.Model):
    """ 用户详细信息 """
    SEX_CHOICES = (
        (1, '男'),
        (0, '女'),
    )
    # username字段为冗余字段，方便查询
    username = models.CharField(verbose_name='用户名', max_length=64, unique=True, editable=False)
    user = models.OneToOneField(verbose_name='关联用户', to=User, related_name='profile', on_delete=models.CASCADE)
    real_name = models.CharField(verbose_name='真实姓名', max_length=32)
    email = models.CharField(verbose_name='邮箱地址', max_length=128, null=True, blank=True)
    is_email_valid = models.BooleanField(verbose_name='邮箱是否已验证', default=False)
    phone_no = models.CharField(verbose_name='手机号码', max_length=20, null=True, blank=True)
    is_phone_valid = models.BooleanField(verbose_name='手机号是否已验证', default=False)
    sex = models.SmallIntegerField(verbose_name='性别', default=1, choices=SEX_CHOICES)
    age = models.SmallIntegerField(verbose_name='年龄', default=0)

    source = models.CharField(verbose_name='登录的来源', max_length=16, null=True)
    version = models.CharField(verbose_name='登录的版本', max_length=16, null=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = '用户详细信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class LoginRecord(models.Model):
    """ 用户登录日志 """
    user = models.ForeignKey(verbose_name='关联用户', to=User, related_name='login_records', on_delete=models.CASCADE)
    username = models.CharField(verbose_name='用户名', max_length=64)
    ip = models.CharField(verbose_name='IP', max_length=32)
    address = models.CharField(verbose_name='地址', max_length=32, null=True, blank=True)
    source = models.CharField(verbose_name='登录的来源', max_length=16, null=True)
    version = models.CharField(verbose_name='登录的版本', max_length=16, null=True)
    created_at = models.DateTimeField(verbose_name='登录时间', auto_now_add=True)

    class Meta:
        db_table = 'accounts_login_record'
