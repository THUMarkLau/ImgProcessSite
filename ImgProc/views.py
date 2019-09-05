from django.shortcuts import render, HttpResponse, redirect
from . import models
from . import utils
import hashlib
import pdb
import numpy as np
import io
import requests

# Create your views here.

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
        pdb.set_trace()
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
        url = request.POST['link']
        resp = requests.get(url)
        image = io.BytesIO(resp.content)
    img_array = utils.byte2Img(image)
    # TODO：调用一个图片识别的接口，传入ndarray，返回结果

    return HttpResponse('123')