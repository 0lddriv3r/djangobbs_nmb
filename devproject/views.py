import os
import re
import time
import glob
import hashlib
import requests
import cv2 as cv
from .forms import *
from .models import *
import urllib.request
from PIL import Image
from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
pagesize = 10


def index(request):
    authorid = request.session.get("authorid", None)
    username = request.session.get("username", None)

    errmsg_sider = request.session.get('errmsg_sider', None)
    errmsg_center = request.session.get('errmsg_center', None)

    categorys = Category.objects.all().order_by('index')
    threads = Thread.objects.all().order_by('-updatetime')

    paginator = Paginator(threads, pagesize, )
    threads = paginator.get_page(1)

    if not authorid:
        rend = render(request, 'index.html',
                      {'threads': threads, 'categorys': categorys, 'authorid': None, 'username': None,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': 'comprehensive'})
    else:
        rend = render(request, 'index.html',
                      {'threads': threads, 'categorys': categorys, 'username': username, 'authorid': authorid,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center,
                       'categoryactive': 'comprehensive'})

    request.session['errmsg_sider'] = None
    request.session['errmsg_center'] = None

    return rend


def page(request, categorynick, pageindex):
    authorid = request.session.get("authorid", None)
    username = request.session.get("username", None)

    errmsg_sider = request.session.get('errmsg_sider', None)
    errmsg_center = request.session.get('errmsg_center', None)

    if categorynick == 'comprehensive':
        threads = Thread.objects.all().order_by('-updatetime')
    else:
        threads = Thread.objects.filter(category=Category.objects.get(nickname=categorynick)).order_by('-updatetime')

    paginator = Paginator(threads, pagesize, )

    try:
        threads = paginator.get_page(pageindex)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)

    categorys = Category.objects.all().order_by('index')

    if not authorid:
        rend = render(request, 'index.html',
                      {'threads': threads, 'categorys': categorys, 'authorid': None, 'username': None,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick})
    else:
        rend = render(request, 'index.html',
                      {'threads': threads, 'categorys': categorys, 'username': username, 'authorid': authorid,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick})

    request.session['errmsg_sider'] = None
    request.session['errmsg_center'] = None

    return rend


def detail(request, categorynick, threadid):
    authorid = request.session.get("authorid", None)
    username = request.session.get("username", None)

    errmsg_sider = request.session.get('errmsg_sider', None)
    errmsg_center = request.session.get('errmsg_center', None)

    categorys = Category.objects.all().order_by('index')

    nexttopicid = 0
    thread = Thread.objects.get(id=threadid)
    threads = Thread.objects.filter(category=Category.objects.get(nickname=categorynick)).all()
    if threads:
        for threadtemp in threads:
            if threadtemp.id > threadid:
                nexttopicid = threadtemp.id
                break

    comments = Comment.objects.filter(thread=thread).order_by('createtime')

    paginator = Paginator(comments, pagesize, )
    comments = paginator.page(1)

    if not authorid:
        rend = render(request, 'detail.html',
                      {'thread': thread, 'categorys': categorys, 'authorid': None, 'username': None,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick,
                       'comments': comments, 'nexttopicid': nexttopicid})
    else:
        rend = render(request, 'detail.html',
                      {'thread': thread, 'categorys': categorys, 'username': username, 'authorid': authorid,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick,
                       'comments': comments, 'nexttopicid': nexttopicid})

    request.session['errmsg_sider'] = None
    request.session['errmsg_center'] = None

    return rend


def detailnext(request, categorynick, threadid):
    authorid = request.session.get("authorid", None)
    username = request.session.get("username", None)

    errmsg_sider = request.session.get('errmsg_sider', None)
    errmsg_center = request.session.get('errmsg_center', None)

    categorys = Category.objects.all().order_by('index')

    nexttopicid = 0
    thread = Thread.objects.get(id=threadid)
    threads = Thread.objects.filter(category=Category.objects.get(nickname=categorynick)).all()
    if threads:
        for threadtemp in threads:
            if threadtemp.id > threadid:
                nexttopicid = threadtemp.id
                break

    comments = Comment.objects.filter(thread=thread).order_by('createtime')

    paginator = Paginator(comments, pagesize, )
    comments = paginator.page(1)

    if not authorid:
        rend = render(request, 'detail.html',
                      {'thread': thread, 'categorys': categorys, 'authorid': None, 'username': None,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick,
                       'comments': comments, 'nexttopicid': nexttopicid})
    else:
        rend = render(request, 'detail.html',
                      {'thread': thread, 'categorys': categorys, 'username': username, 'authorid': authorid,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick,
                       'comments': comments, 'nexttopicid': nexttopicid})

    request.session['errmsg_sider'] = None
    request.session['errmsg_center'] = None

    return rend


def detailpage(request, categorynick, threadid, pageindex):
    authorid = request.session.get("authorid", None)
    username = request.session.get("username", None)

    errmsg_sider = request.session.get('errmsg_sider', None)
    errmsg_center = request.session.get('errmsg_center', None)

    categorys = Category.objects.all().order_by('index')
    thread = Thread.objects.get(id=threadid)
    comments = Comment.objects.filter(thread=thread).order_by('createtime')

    paginator = Paginator(comments, pagesize, )

    try:
        comments = paginator.get_page(pageindex)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    if not authorid:
        rend = render(request, 'detail.html',
                      {'thread': thread, 'categorys': categorys, 'authorid': None, 'username': None,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick,
                       'comments': comments})
    else:
        rend = render(request, 'detail.html',
                      {'thread': thread, 'categorys': categorys, 'username': username, 'authorid': authorid,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick,
                       'comments': comments})

    request.session['errmsg_sider'] = None
    request.session['errmsg_center'] = None

    return rend


def category(request, categorynick):
    authorid = request.session.get("authorid", None)
    username = request.session.get("username", None)

    errmsg_sider = request.session.get('errmsg_sider', None)
    errmsg_center = request.session.get('errmsg_center', None)

    if categorynick == 'comprehensive':
        threads = Thread.objects.all().order_by('-updatetime')
    else:
        threads = Thread.objects.filter(category=Category.objects.get(nickname=categorynick)).order_by('-updatetime')

    paginator = Paginator(threads, pagesize, )
    threads = paginator.page(1)

    categorys = Category.objects.all().order_by('index')

    if not authorid:
        rend = render(request, 'index.html',
                      {'threads': threads, 'categorys': categorys, 'authorid': None, 'username': None,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick})
    else:
        rend = render(request, 'index.html',
                      {'threads': threads, 'categorys': categorys, 'username': username, 'authorid': authorid,
                       'errmsg_sider': errmsg_sider, 'errmsg_center': errmsg_center, 'categoryactive': categorynick})

    request.session['errmsg_sider'] = None
    request.session['errmsg_center'] = None

    return rend


def login(request):
    form = UserForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        ipaddr = request.META['REMOTE_ADDR']

        flag = True
        try:
            Black.objects.get(ipaddr=ipaddr)
        except Black.DoesNotExist:
            flag = False

        if flag:
            return render(request, 'black.html')

        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', username):
            request.session['errmsg_sider'] = '不可以包含非法字符！'
            return HttpResponseRedirect('/')

        try:
            userobj = User.objects.get(username=str(username))
        except User.DoesNotExist:
            request.session['errmsg_sider'] = '用户名或密码错误！'
            return HttpResponseRedirect('/')

    if userobj.password == password:
        request.session['authorid'] = userobj.id
        request.session['username'] = userobj.username
    else:
        request.session['errmsg_sider'] = '用户名或密码错误！'

    return HttpResponseRedirect('/')


def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        email = data['email'].strip()
        username = data['username'].strip()
        password = data['password'].strip()
        ipaddr = request.META['REMOTE_ADDR']

        flag = True
        try:
            Black.objects.get(ipaddr=ipaddr)
        except Black.DoesNotExist:
            flag = False

        if flag:
            return render(request, 'black.html')

        if len(username) <= 4 and len(username) >= 14:
            request.session['errmsg_sider'] = '用户名长度只能在4到14个字符之间！'
            return HttpResponseRedirect('/')

        if len(username) <= 4 and len(username) >= 14:
            request.session['errmsg_sider'] = '密码长度只能在4到14个字符之间！'
            return HttpResponseRedirect('/')
            
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', username):
            request.session['errmsg_sider'] = '不可以包含非法字符！'
            return HttpResponseRedirect('/')

        try:
            validate_email(email)
        except ValidationError:
            request.session['errmsg_sider'] = '邮箱格式错误！'
            return HttpResponseRedirect('/')

        m = hashlib.md5()
        m.update(email.encode("utf-8"))
        avator = 'http://www.gravatar.com/avatar/' + m.hexdigest() + '?s=50'

        flag = 0
        try:
            User.objects.get(username=str(username))
        except User.DoesNotExist:
            flag += 1

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            flag += 1

        if flag == 2:
            userobj = User.objects.create(username=str(username), password=str(password), email=email, avator=avator,
                                          ipaddr=ipaddr)
            request.session['authorid'] = userobj.id
            request.session['username'] = userobj.username
        else:
            request.session['errmsg_sider'] = '用户名或邮箱已存在！'

        return HttpResponseRedirect('/')

    request.session['errmsg_sider'] = '填写的数据有误！'
    return HttpResponseRedirect('/')


def logout(request):
    if not request.session.get('username', None):
        request.session['errmsg_sider'] = '未登录！'
        return HttpResponseRedirect('/')

    request.session.flush()
    return HttpResponseRedirect('/')


def search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        keyword = data['keyword']

        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', keyword):
            request.session['errmsg_keyword'] = '不可以包含非法字符！'
            return HttpResponseRedirect('/')

        threads = Thread.objects.filter(title__icontains=keyword)
        if len(threads) > 10:
            threads = threads[:10]

        authorid = request.session.get("authorid", None)
        username = request.session.get("username", None)

        categorys = Category.objects.all().order_by('index')

        if not authorid:
            rend = render(request, 'index.html',
                          {'threads': threads, 'categorys': categorys, 'authorid': None, 'username': None,
                           'categoryactive': 'comprehensive'})
        else:
            rend = render(request, 'index.html',
                          {'threads': threads, 'categorys': categorys, 'username': username, 'authorid': authorid,
                           'categoryactive': 'comprehensive'})

        return rend

    request.session['errmsg_keyword'] = '输入关键词错误！'
    return HttpResponseRedirect('/')


def searchphoto(request):
    form = SearchPhotoForm(request.POST, request.FILES)
    if form.is_valid():
        imgkey = form.cleaned_data['imgkey']

        ext = os.path.splitext(imgkey.name)[1]
        if ext != '.jpg' and ext != '.png':
            return JsonResponse({'res': '图片格式不支持！'})

        if imgkey.size > 6291456:
            return JsonResponse({'res': '图片大小不能超过6兆！'})

        flag = False
        basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ext = os.path.splitext(imgkey.name)[1]

        dir = '/static/chimg/'
        filename = str(int(time.time()))
        filepath = dir + filename + ext

        f = open(basepath + filepath, 'wb')
        for line in imgkey.chunks():
            f.write(line)
        f.close()

        if imgkey.size > 1572864:
            if ext == '.png':
                png2jpg(basepath + filepath)

            realpath = dir + filename + '.jpg'
            for infile in glob.glob(basepath + realpath):
                im = Image.open(infile)
                size = im.size
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(basepath + realpath, 'jpeg')
            flag = True

        if flag:
            path = realpath
        else:
            path = filepath

        filename, ext2 = os.path.splitext(path)

        files = None
        if ext2 == '.jpg':
            files = {'file': (filename + ext2, open(basepath + path, 'rb'), 'image/jpeg', {})}
        else:
            files = {'file': (filename + ext2, open(basepath + path, 'rb'), 'image/png', {})}

        res = requests.post(url='http://saucenao.com/search.php', files=files)
        obj = re.search(r'"https://danbooru.donmai.us/(.*?)"', res.text)

        if obj:
            return JsonResponse({'res': obj.group(0).replace(r'"', '')})
        else:
            return JsonResponse({'res': '没有发现这张图片呢~'})

    return JsonResponse({'res': '上传出现错误！'})


def publish(request):
    username = request.session.get('username', None)
    if not username:
        request.session['errmsg_center'] = '未登录！'
        return HttpResponseRedirect('/')

    flag = True
    try:
        userobj = User.objects.get(username=str(username))
        Black.objects.get(ipaddr=userobj.ipaddr)
    except Black.DoesNotExist:
        flag = False

    if flag:
        return render(request, 'black.html')

    category = None
    form = ThreadForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.cleaned_data
        body = data['body']
        title = data['title']
        authorid = data['authorid']
        attachment = form.cleaned_data['attachment']
        category = request.POST.get('category')
        musicurl = data['musicurl']

        if len(title) >= 50:
            request.session['errmsg_center'] = '标题长度不能大于50个字符！'
            return HttpResponseRedirect('/category/' + category)

        if len(body) >= 10000:
            request.session['errmsg_center'] = '内容长度不能大于10000个字符！'
            return HttpResponseRedirect('/category/' + category)

        if musicurl:
            ext = os.path.splitext(musicurl)[1]
            if ext != '.mp3':
                request.session['errmsg_center'] = 'MP3链接格式错误！'
                return HttpResponseRedirect('/category/' + category)

            try:
                with urllib.request.urlopen(musicurl) as file:
                    flag = False
            except urllib.request.URLError:
                flag = True

            if flag:
                request.session['errmsg_center'] = 'MP3链接可能失效了！'
                return HttpResponseRedirect('/category/' + category)

        if attachment:
            ext = os.path.splitext(attachment.name)[1]
            if ext != '.jpg' and ext != '.png':
                request.session['errmsg_center'] = '图片格式不支持！'
                return HttpResponseRedirect('/category/' + category)

            if attachment.size > 6291456:
                request.session['errmsg_center'] = '图片大小不能超过6兆！'
                return HttpResponseRedirect('/category/' + category)

        if not title:
            title = '无标题'

        path = None
        if attachment:
            basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ext = os.path.splitext(attachment.name)[1]

            dir = '/static/img/'
            filename = str(int(time.time()))
            filepath = dir + filename + ext

            f = open(basepath + filepath, 'wb')
            for line in attachment.chunks():
                f.write(line)
            f.close()

            if attachment.size > 1572864:
                if ext == '.png':
                    png2jpg(basepath + filepath)

                realpath = dir + filename + '.jpg'
                for infile in glob.glob(basepath + realpath):
                    im = Image.open(infile)
                    size = im.size
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(basepath + realpath, 'jpeg')
                flag = True

            if flag:
                path = realpath
            else:
                path = filepath

        author = User.objects.get(id=authorid)
        category = Category.objects.get(nickname=category)

        Thread.objects.create(title=title, body=body, author=author, attachment=path, category=category,
                              musicurl=musicurl)

        return HttpResponseRedirect('/category/' + category.nickname)

    request.session['errmsg_center'] = '信息输入错误'
    return HttpResponseRedirect('/category/' + category.nickname)


def comment(request):
    username = request.session.get('username', None)
    if not username:
        request.session['errmsg_center'] = '未登录！'
        return HttpResponseRedirect('/')

    flag = True
    try:
        userobj = User.objects.get(username=str(username))
        Black.objects.get(ipaddr=userobj.ipaddr)
    except Black.DoesNotExist:
        flag = False

    if flag:
        return render(request, 'black.html')

    thread = None
    category = None
    form = CommentForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.cleaned_data
        body = data['body']
        title = data['title']
        threadid = data['threadid']
        authorid = data['authorid']
        attachment = form.cleaned_data['attachment']
        categoryactive = data['categoryactive']
        musicurl = data['musicurl']

        if len(title) >= 50:
            request.session['errmsg_center'] = '标题长度不能大于50个字符！'
            return HttpResponseRedirect('/category/' + categoryactive + '/thread/' + str(threadid))

        if len(body) >= 10000:
            request.session['errmsg_center'] = '内容长度不能大于10000个字符！'
            return HttpResponseRedirect('/category/' + categoryactive + '/thread/' + str(threadid))

        if musicurl:
            ext = os.path.splitext(musicurl)[1]
            if ext != '.mp3':
                request.session['errmsg_center'] = 'MP3链接格式错误！'
                return HttpResponseRedirect('/category/' + categoryactive + '/thread/' + str(threadid))

            flag = False
            try:
                with urllib.request.urlopen(musicurl) as file:
                    flag = False
            except urllib.request.URLError:
                flag = True

            if flag:
                request.session['errmsg_center'] = 'MP3链接可能失效了！'
                return HttpResponseRedirect('/category/' + categoryactive + '/thread/' + str(threadid))

        if attachment:
            ext = os.path.splitext(attachment.name)[1]
            if ext != '.jpg' and ext != '.png':
                request.session['errmsg_center'] = '图片格式不支持！'
                return HttpResponseRedirect('/category/' + categoryactive + '/thread/' + str(threadid))

            if attachment.size > 6291456:
                request.session['errmsg_center'] = '图片大小不能超过6兆！'
                return HttpResponseRedirect('/category/' + categoryactive + '/thread/' + str(threadid))

        if not title:
            title = '无标题'

        path = None
        if attachment:
            basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ext = os.path.splitext(attachment.name)[1]

            dir = '/static/img/'
            filename = str(int(time.time()))
            filepath = dir + filename + ext

            f = open(basepath + filepath, 'wb')
            for line in attachment.chunks():
                f.write(line)
            f.close()

            if attachment.size > 1572864:
                if ext == '.png':
                    png2jpg(basepath + filepath)

                realpath = dir + filename + '.jpg'
                for infile in glob.glob(basepath + realpath):
                    im = Image.open(infile)
                    size = im.size
                    im.thumbnail(size, Image.ANTIALIAS)
                    im.save(basepath + realpath, 'jpeg')
                flag = True

            if flag:
                path = realpath
            else:
                path = filepath

        author = User.objects.get(id=authorid)
        thread = Thread.objects.get(id=threadid)
        thread.commentnum = thread.commentnum + 1
        thread.save()

        category = Category.objects.get(nickname=categoryactive)
        Comment.objects.create(title=title, body=body, author=author, attachment=path, thread=thread,
                               musicurl=musicurl, floor=thread.commentnum)

        return HttpResponseRedirect('/category/' + category.nickname + '/thread/' + str(thread.id))

    request.session['errmsg_center'] = '信息输入错误'
    return HttpResponseRedirect('/category/' + category.nickname + '/thread/' + str(thread.id))


def png2jpg(path):
    img = cv.imread(path, 0)
    w, h = img.shape[::-1]
    infile = path
    outfile = os.path.splitext(infile)[0] + ".jpg"
    img = Image.open(infile)
    try:
        if len(img.split()) == 4:
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.convert('RGB').save(outfile, quality=100)
            os.remove(path)
        else:
            img.convert('RGB').save(outfile, quality=100)
            os.remove(path)
        return outfile
    except Exception as e:
        pass
