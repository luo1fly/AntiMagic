#!/usr/bin/env python
# Name: utils.py
# Time:8/12/16 3:03 PM
# Author:luo1fly

import datetime
import random
import os
from AntiMagic import settings
# import custom modules above


def datetime_to_strftime(time_instance):
    if isinstance(time_instance, datetime.datetime):
        return time_instance.strftime('%Y-%m-%d %H:%M:%S')


def handle_upload_file(request, file_obj):
    random_dir = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890', 10))
    upload_dir = '%s/%s' % (settings.FileUploadDir, request.user.id)
    # 给文件添加一级随机目录，避免出现重名问题
    upload_dir2 = '%s/%s' % (upload_dir, random_dir)

    if not os.path.isdir(upload_dir2):
        os.makedirs(upload_dir2)    # 注意和mkdir用法的不同，makedirs可递归

    with open('%s/%s' % (upload_dir2, file_obj.name), 'wb') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    return "%s/%s" % (random_dir, file_obj.name)    # 返回给视图函数，由视图函数调用后台脚本分发文件到远程主机
