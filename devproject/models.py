from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(models.Model):
    '''用户模型类'''
    avator = models.URLField('头像')
    password = models.CharField('密码', max_length=255)
    ipaddr = models.GenericIPAddressField('地址', null=True)
    email = models.CharField('邮箱', max_length=255, unique=True)
    username = models.CharField('昵称', max_length=128, unique=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建')
    lastpublishtime = models.DateTimeField(auto_now=True, verbose_name='最后')

    class Meta:
        ordering = ['createtime']
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Category(models.Model):
    '''类别模型类'''
    name = models.CharField('类别', max_length=20)
    index = models.IntegerField('排序', default=0)
    nickname = models.CharField('匿名', max_length=20)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建')

    class Meta:
        ordering = ['createtime']
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Thread(models.Model):
    '''线程模型类'''
    body = models.TextField('正文', default='')
    commentnum = models.IntegerField('评论', default=0)
    title = models.CharField('标题', max_length=100, null=True)
    attachment = models.TextField('附件', blank=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建')
    musicurl = models.CharField('音乐', max_length=300, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='类别')

    class Meta:
        ordering = ['createtime']
        verbose_name = '线程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''评论模型类'''
    body = models.TextField('正文', default='')
    floor = models.IntegerField('楼层', default=1)
    title = models.CharField('标题', max_length=100, null=True)
    attachment = models.TextField('附件', blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    musicurl = models.CharField('音乐', max_length=300, blank=True, null=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE, )
    thread = models.ForeignKey(Thread, verbose_name='线程', on_delete=models.CASCADE, )

    class Meta:
        ordering = ['createtime']
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body


class Black(models.Model):
    '''黑名单模型类'''
    ipaddr = models.GenericIPAddressField('地址')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建')

    class Meta:
        ordering = ['createtime']
        verbose_name = '黑单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ipaddr
