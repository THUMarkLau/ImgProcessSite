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


class Record(models.Model):
    '''
    用户上传记录，包含原图片和结果图片
    ---------------
    src_img -> 原始图片
    res_img -> 处理后的结果
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    src_img = models.ImageField(upload_to="%Y/%m/%d/%H/%M/%S" + '/src/',null=True)
    res_img = models.ImageField(upload_to="%Y/%m/%d/%H/%M/%S" + '/res/',null=True)
    time = models.FloatField(default=0.0)
    date = models.DateField(auto_now=True)
    t = models.TimeField(auto_now=True)
