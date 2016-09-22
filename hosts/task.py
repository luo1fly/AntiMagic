#!/usr/bin/env python
# Name: task.py
# Time:8/11/16 10:23 AM
# Author:luo1fly

from django.db import transaction
from hosts import models
import subprocess
from AntiMagic import settings
import os
import json
# from django.utils.datastructures import MultiValueDictKeyError
# import your modules above


class Task(object):
    def __init__(self, request):
        self.request = request

    def call(self, task_type):
        func = getattr(self, task_type)
        return func()

    @transaction.atomic
    def multi_cmd(self):
        # print('---going to run cmd----', self.request.POST['task_type'])
        task_obj = models.TaskLog(
            task_type=self.request.POST['task_type'],
            user_id=self.request.user.id,   # foreign_key user_id not user
            # hosts many to many records should be added after task_obj created
            cmd=self.request.POST['cmd'],
        )
        task_obj.save()
        hosts_list = set(self.request.POST.getlist('selected_hosts[]'))
        # need to be unique
        # print(hosts_list)
        task_obj.hosts.add(*hosts_list)

        # 为选中的host2user记录分别创建任务记录到详细表中
        for bind_host_id in hosts_list:
            # one task then iterate host_id
            task_log_detail_obj = models.TaskLogDetail(
                child_of_task_id=task_obj.id,
                bind_host_id=bind_host_id,
                event_log='N/A'
            )
            task_log_detail_obj.save()

        # print(settings.MultiTaskScript,str(task_obj.id),settings.MultiTaskRunType)
        p = subprocess.Popen(
            [
                'python',
                settings.MultiTaskScript,
                '-i', str(task_obj.id),
                '-t', settings.MultiTaskRunType
            ],
            preexec_fn=os.setsid
        )
        print('------>', p.pid)

        return task_obj.id

    @transaction.atomic
    def multi_file_delivery(self):
        task_type = self.request.POST['file_transfer_type']
        selected_hosts = set(self.request.POST.getlist("selected_hosts[]"))
        upload_files = self.request.POST.getlist('upload_files[]')
        cmd_dic = dict(
            remote_path=self.request.POST['remote_path'],
            upload_files=upload_files,
        )

        task_obj = models.TaskLog(
            task_type=task_type,
            user_id=self.request.user.id,
            cmd=json.dumps(cmd_dic),
        )
        task_obj.save()
        task_obj.hosts.add(*selected_hosts)
        # m2m关系需要先创建对象再添加，无需再次保存

        for host_id in selected_hosts:
            task_log_detail_obj = models.TaskLogDetail(
                child_of_task_id=task_obj.id,
                bind_host_id=host_id,
                event_log='N/A',
            )
            task_log_detail_obj.save()

        p = subprocess.Popen(
            [
                'python',
                settings.MultiTaskScript,
                '-i', str(task_obj.id),
                '-t', settings.MultiTaskRunType
            ],
            preexec_fn=os.setsid
        )
        print('------>', p.pid)

        return task_obj.id

    def get_task_result(self):
        task_id = self.request.GET.get('task_id')
        if task_id:
            task_obj_list = models.TaskLogDetail.objects.filter(child_of_task_id=task_id)
            task_result_list = list(task_obj_list.values(
                'id',
                'date',
                'event_log',
                'result',
                'note',
                'bind_host__host__name',    # 通过bind_host_id反查到对应host表中的name
                'bind_host__host__ip_address',  # 通过bind_host_id反查到对应的host表中的ip_address字段
                'bind_host__host_user__username'    # 通过bind_host_id反查到host_user表中的username字段
            ))
            return task_result_list


