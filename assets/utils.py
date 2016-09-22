#!/usr/bin/env python
# Name: utils.py
# Time:8/19/16 3:38 PM
# Author:luo1fly

import time, hashlib, json, datetime
from hosts import models as hosts_models
from django.shortcuts import render, HttpResponse
from AntiMagic import settings
from django.core.exceptions import ObjectDoesNotExist
import redis
# import custom modules above

R = redis.Redis('192.168.0.195')


def json_date_handler(obj):
    # if hasattr(obj, 'isoformat'):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d")


def json_datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")


def gen_token(username, timestamp, token):
    token_format = "%s\n%s\n%s" %(username, timestamp, token)
    obj = hashlib.md5()
    obj.update(token_format.encode('utf8'))
    # print '--->token format:[%s]'% token_format
    return obj.hexdigest()[10:17]


def push_token_into_redis(token):
    """
    :param token: usertoken
    :return:
    """
    R.set(token, 1, ex=settings.TOKEN_TIMEOUT)


def token_exist_in_redis(token):
    """
    :param token: usertoken
    :return:
    """
    if R.get(token):
        return True
    else:
        return False


def token_required(func):
    def wrapper(*args, **kwargs):
        response = {"errors": []}

        get_args = args[0].GET
        username = get_args.get("user")
        token_md5_from_client = get_args.get("token")
        timestamp = get_args.get("timestamp")
        if not username or not timestamp or not token_md5_from_client:
            response['errors'].append({"auth_failed": "This api requires token authentication!"})
            return HttpResponse(json.dumps(response))
        try:
            user_obj = hosts_models.UserProfile.objects.get(email=username)
            token_md5_from_server = gen_token(username, timestamp, user_obj.token)
            if token_md5_from_client != token_md5_from_server:
                response['errors'].append({"auth_failed": "Invalid username or token_id"})
            else:
                if abs(time.time() - int(timestamp)) > settings.TOKEN_TIMEOUT:
                    # default timeout 120
                    response['errors'].append({"auth_failed": "The token is expired!"})
                else:
                    if token_exist_in_redis(token_md5_from_client):
                        response['errors'].append({"auth_failed": "The token has been used!"})
                        # redis里已有的key被认为已使用过
                print(
                    "\033[41;1m;%s ---client:%s\033[0m" % (time.time(), timestamp),
                    time.time() - int(timestamp)
                )
        except ObjectDoesNotExist as e:
            response['errors'].append({"auth_failed": "Invalid username or token_id"})
        if response['errors']:
            return HttpResponse(json.dumps(response))
        else:
            push_token_into_redis(token_md5_from_client)
            # 认证成功的token存到redis
            return func(*args, **kwargs)
    return wrapper
