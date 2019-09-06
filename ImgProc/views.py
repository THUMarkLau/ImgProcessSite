from django.shortcuts import render, HttpResponse, redirect
from . import utils
import hashlib
import pdb
import numpy as np
import io
import requests
from . import models
import time

# Create your views here.

# 图片所占用网页的高度
pic_height = 175
# 图片所占用网页的比例
pic_perc = 55

def index(request):
    '''访问主界面，返回主界面网页'''
    try:
        cookie = request.COOKIES['id']
        user = models.User.objects.get(cookie=cookie)
        return userMainPage(request)
    except:
        return render(request, 'index.html')

def regist(request):
    '''注册系统，密码不得少于5位，用户名不得重复'''
    username = request.POST['username']
    password = request.POST['password']
    # 查询该用户名是否被注册
    try:
        user_obj = models.User.objects.get(username=username)
        # 已被注册
        return render(request, 'base.html', {
            'title' : 'Regist Fail',
            'header' : 'IMP',
            'paras' : [
                '''Fail to regist, because the username has been 
                registed. Please try again.'''
            ]
        })
    except models.User.DoesNotExist:
        # 未注册
        pass
    if len(password) < 5:
        return render(request, 'base.html', {
            'title' : 'Regist Fail',
            'header' : 'IMP',
            'paras' : [
                '''Fail to regist, because the password is too short.
                Please try again.'''
            ]
        })
    pwd = hashlib.md5()
    pwd.update(password.encode(encoding='utf-8'))
    password = str(pwd.hexdigest())
    user = models.User(username=username, password=password)
    user.save()
    return render(request, 'base.html', {
        'title' : 'Regist Success',
        'header' : 'IMP',
        'paras':[
            'success',
        ]
    })

def login(request):
    '''登录系统，使用 POST 方式'''
    username = request.POST['username']
    password = request.POST['password']
    # 判断是否存在该用户
    try:
        user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        # 未找到该用户
        return render(request, 'base.html', {
            'title' : 'Login Fail',
            'header' : 'IMP',
            'paras': [
                'Login fail, because user ' + username + ' does not exist.'
            ]
        })
    # 加密密码
    psw = hashlib.md5()
    psw.update(password.encode(encoding='utf-8'))
    if user.password == str(psw.hexdigest()):
        # 登录成功
        response = userMainPage(request)
        cookie = str(hash(username))
        user.cookie = cookie[:100]
        user.save()
        response.set_cookie('id', cookie[:100])
        return response
    else:
        # 密码错误，登录失败
        return render(request, 'base.html', {
            'title' : 'Login Fail',
            'header' : 'IMP',
            'paras' : [
                'Login fail, because password is wrong. Please try again.'
            ]
        })

def logout(request):
    '''用户注销'''
    try:
        cookie = request.COOKIES['id']
        user = models.User.objects.get(cookie=cookie)
        user.cookie = ''
        user.save()
    except:
        pass
    return redirect(index)

def userMainPage(request):
    '''用户主页'''
    try:
        username = request.POST['username']
    except KeyError:
        cookie = request.COOKIES['id']
        user = models.User.objects.get(cookie=cookie)
        username = user.username
    return render(request, 'user.html', {
        'username':username
    })

def processImg(request):
    '''接受上传的图片，并调用接口进行处理'''
    try:
        # 通过上传文件的形式来获得图片
        image = request.FILES['img']
        # 检查文件类型
        if 'image' not in image.content_type:
            # 如果上传的不是图片类型
            return render(request, 'base.html', {
                'title' : 'Error',
                'header' : 'IMP',
                'title' : 'Upload File Fail',
                'paras' : [
                    'Failed to upload file, because the file is not image type. Please try again.'
                ]
            })
    except KeyError:
        # 通过 url 的方式获取图片
        # 获取链接
        url = request.POST['link']
        # 通过网络获取内容
        resp = requests.get(url)
        # 转换为BytesIO类型，方便后面统一接口
        image = io.BytesIO(resp.content)
    # 将BytesIO类的图片转化为ndarray类型的图片
    img_array = utils.byte2Img(image)
    # TODO：调用一个图片识别的接口，传入ndarray，返回结果
    # 寻找对应的用户
    id = request.COOKIES['id']
    user = models.User.objects.get(cookie=id)
    # 获取当前时间
    id = time.time()
    # 生成记录
    user.record_set.create(src_img = image, time=id)
    # 返回结果
    return render(request, 'result.html', {
        'src_img' : user.record_set.get(time=id).src_img
    })

def userRecord(request, page=0):
    '''查看用户的使用记录'''
    # 寻找对应的用户
    id = request.COOKIES['id']
    try:
        page = int(page)
    except:
        return HttpResponse("Wrong URL")
    user = models.User.objects.get(cookie=id)
    records = user.record_set.all()
    # 判断访问是否越界，是则返回第一页
    if page * 10 > len(records):
        return render(request, 'record.html', {
            'page':0,
            'next':True,
            "length" : pic_perc * len(records[0:10]),
            "height" : pic_height * len(records[0:10])
        })
    return render(request, 'record.html', {
        'records':records[page*10:page*10 + 10],
        'page' : page + 1 if (page+1)*10 < len(records)  else 0,
        'next' : True,
        "length" : pic_perc * len(records[page*10:page*10 + 10]),
        "height" : pic_height * len(records[page*10 : page*10 + 10]),
        "username" : user.username
    })

def deleteRecord(request, id):
    '''删除用户记录'''
    # 检查用户身份
    cookie = request.COOKIES['id']
    try:
        user = models.User.objects.get(cookie=cookie)
    except models.User.DoesNotExist:
        return redirect(index)
    # 用户验证成功
    # 删除记录
    record = user.record_set.get(id=id)
    record.delete()
    # 删除成功
    return render(request, 'base.html', {
        'T' : 'Delete Success',
        'header' : 'IMP',
        'title' : 'Delete Success',
        'paras' : {
            'Delete Success!'
        }
    })

def queryPage(request):
    '''返回查询页面'''
    return render(request, 'query.html')

def queryRecord(request):
    '''查询记录'''
    # 获取查询的时间段参数

    from_datetime = request.POST['from_date'] + ' ' + request.POST['from_time']
    to_datetime = request.POST['to_date'] + ' ' + request.POST['to_time']
    # 将查询时间转换为时间戳
    from_time = timeTrans(from_datetime)
    to_time = timeTrans(to_datetime)
    # 获取cookies，查找用户
    id = request.COOKIES['id']
    try:
        user = models.User.objects.get(cookie = id)
    except models.User.DoesNotExist:
        # 用户不存在，返回主页
        return index(request)
    records = user.record_set.filter(time__lte=to_time, time__gte=from_time)
    pdb.set_trace()
    return render(request, "record.html", {
        'records' : records,
        'next' : False,
        "length" : pic_perc * len(records),
        "height" : pic_height * len(records)
    })

def timeTrans(time_string, string_mode = '%Y-%m-%d %H:%M'):
    '''将格式化的时间字符串转换为时间戳'''
    time_array = time.strptime(time_string, string_mode)
    return int(time.mktime(time_array))
