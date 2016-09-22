from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from hosts import models, task, utils
import json
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html', locals())


@login_required
def hosts_index(request):
    return render(request, 'hosts/dashboard.html', locals())


@login_required
def host_mgr(request):
    try:
        group_id = request.GET['groupid']
    except MultiValueDictKeyError as e:
        host_list = request.user.bind_hosts.select_related()
        group_name = '未分组'
    else:
        host_list = models.BindHostToUser.objects.filter(host_groups__id=group_id)
        group_name = models.HostGroup.objects.get(id=group_id)
    # print(locals())
    return render(request, 'hosts/host_mgr.html', locals())


@login_required
def multi_cmd(request):
    return render(request, 'hosts/multi_cmd.html', locals())


@login_required
def submit_task(request):
    try:
        task_type = request.POST['task_type']
    except MultiValueDictKeyError as e:
        return HttpResponse('chu cuo le, ni mei you chuan task_type')
    else:
        task_handler = task.Task(request)
        task_id = task_handler.call(task_type)  # backend func() returns
        return HttpResponse(json.dumps(task_id))


@login_required
def get_task_result(request):
    task_handler = task.Task(request)
    task_result = task_handler.get_task_result()
    # print(task_result)
    return HttpResponse(json.dumps(task_result, default=utils.datetime_to_strftime))


@login_required
def file_delivery(request):
    return render(request, 'hosts/multi_file_delivery.html', locals())


@csrf_exempt
@login_required
def file_upload(request):
    file_obj = request.FILES['filename']
    file_upload_path = utils.handle_upload_file(request, file_obj)
    return HttpResponse(json.dumps(file_upload_path))


@login_required
def assets_index(request):
    return render(request, 'assets/dashboard.html', locals())


@login_required
def monitor_index(request):
    return render(request, 'monitor/dashboard.html', locals())


@login_required
def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def acc_login(request):
    if request.method == 'GET':    # 如果是GET方法则转到登陆页面
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)    # 如果验证通过，返回值为user对象，反之为None
        if user:
            login(request, user)     # 需要传递一个user对象和request
            # print(request)
            return HttpResponseRedirect('/')
        else:
            login_err = 'Username or Password error!'
            return render(request, 'login.html', locals())      # 将字符串对象传递给模版

