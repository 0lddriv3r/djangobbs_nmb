from django import forms
from .models import Category

categorys = Category.objects.all()

class SearchForm(forms.Form):
    keyword = forms.CharField(label='内容')


class SearchPhotoForm(forms.Form):
    imgkey = forms.FileField(label='图片')


class UserForm(forms.Form):
    password = forms.CharField(label='密码')
    username = forms.CharField(label='用户名')
    email = forms.CharField(label='邮箱', required=False)


class ThreadForm(forms.Form):
    body = forms.CharField(label='内容')
    authorid = forms.CharField(label='作者')
    title = forms.CharField(label='标题', required=False)
    musicurl = forms.CharField(label='音乐', required=False)
    attachment = forms.FileField(label='附件', required=False)


class CommentForm(forms.Form):
    body = forms.CharField(label='内容')
    threadid = forms.CharField(label='线程')
    authorid = forms.CharField(label='作者')
    categoryactive = forms.CharField(label='类别')
    title = forms.CharField(label='标题', required=False)
    musicurl = forms.CharField(label='音乐', required=False)
    attachment = forms.FileField(label='附件', required=False)
