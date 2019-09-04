from django.shortcuts import render, HttpResponse
from . import models
from . import utils
import hashlib

# Create your views here.

def index(request):
    return render(request, 'index.html')

def regist(request):
    username = request.POST['username']
    password = request.POST['password']
    a = utils.Navigation('https://www.baidu.com', 'test')
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
    pwd = hashlib.md5()
    pwd.update(password.encode(encoding='utf-8'))
    password = str(pwd.hexdigest())
    user = models.User(username=username, password=password)
    user.save()
    return render(request, 'base.html', {
        'title' : 'Regist Success',
        'header' : 'IMP',
        'navigation' : '',
        'paras':[
            'success',
        ]
    })