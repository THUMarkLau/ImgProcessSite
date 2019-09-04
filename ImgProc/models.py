from django.db import models

# Create your models here.


class User(models.Model):
    '''
    用户类
    ---------------
    username -> 用户姓名，字符串格式，最长不超过 64 个字符
    password -> 用户密码，字符串格式，最长不超过 64 个字符
    '''
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    cookie = models.CharField(max_length=100, default='')

    def __str__(self):
        return '''username = %s 
                    password = %s''' % (self.username, self.password)