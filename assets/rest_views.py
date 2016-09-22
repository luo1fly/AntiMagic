#!/usr/bin/env python
# Name: rest_views.py
# Time:9/20/16 3:09 PM
# Author:luo1fly

from rest_framework import viewsets
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework import (status, permissions)
from rest_framework.response import Response
from assets import models, serializers
from hosts import models as hosts_models
from assets.utils import token_required
# import custom modules above


class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
    """
    queryset = hosts_models.UserProfile.objects.all().order_by('-date_joined')
    # 数据库查询结果集
    serializer_class = serializers.UserSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = models.Asset.objects.all()
    serializer_class = serializers.AssetSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = models.Server.objects.all()
    serializer_class = serializers.ServerSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def asset_list(request):
    if request.method == 'GET':
        assets_list = models.Asset.objects.all()
        serializer = serializers.AssetSerializer(assets_list, many=True)
        print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)