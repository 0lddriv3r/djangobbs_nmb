from django.contrib import admin
from .models import Thread, User, Black, Comment, Category


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'ipaddr', 'createtime', 'lastpublishtime')


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'category', 'attachment', 'commentnum', 'createtime', 'updatetime')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'nickname', 'index', 'createtime')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'floor', 'attachment', 'createtime')


class BlackAdmin(admin.ModelAdmin):
    list_display = ('ipaddr', 'createtime')


admin.site.register(User, UserAdmin)
admin.site.register(Black, BlackAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
