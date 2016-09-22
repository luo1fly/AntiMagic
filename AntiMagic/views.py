#!/usr/bin/env python
# Name: views.py
# Time:8/18/16 12:59 PM
# Author:luo1fly

from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html')


def acc_login(request):
    if request.method == "POST":

        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            # if timezone.now() > user.valid_begin_time and timezone.now() < user.valid_end_time:
            if user.valid_begin_time < timezone.now() < user.valid_end_time:
                auth.login(request, user)
                request.session.set_expiry(60*30)
                # print 'session expires at :',request.session.get_expiry_date()
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', {
                    'login_err': 'User account is expired,please contact your IT guy for this!'
                })

        else:
            return render(request, 'login.html', {
                'login_err': 'Wrong username or password!'
            })
    else:
        return render(request, 'login.html')