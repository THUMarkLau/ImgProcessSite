# Generated by Django 2.2.4 on 2019-09-05 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImgProc', '0008_auto_20190905_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='res_img',
            field=models.ImageField(null=True, upload_to='%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='record',
            name='src_img',
            field=models.ImageField(null=True, upload_to='%Y/%m/%d/'),
        ),
    ]
