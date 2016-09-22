# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 06:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BindHostToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '主机与用户绑定关系',
                'verbose_name': '主机与用户绑定关系',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('sn', models.CharField(max_length=128)),
                ('ip_address', models.GenericIPAddressField()),
                ('port', models.IntegerField(default=22)),
                ('system_type', models.CharField(choices=[('linux', 'Linux'), ('windows', 'Windows')], default='linux', max_length=32)),
                ('enabled', models.BooleanField(default=1)),
                ('memo', models.TextField(blank=1, null=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '远程主机',
                'verbose_name': '远程主机',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=1)),
                ('memo', models.TextField(blank=1, null=1)),
            ],
            options={
                'verbose_name_plural': '主机组',
                'verbose_name': '主机组',
            },
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_type', models.CharField(choices=[('ssh-password', 'SSH/PASSWORD'), ('ssh-key', 'SSH/KEY')], default='ssh-password', max_length=32)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(blank=1, max_length=128, null=1)),
            ],
            options={
                'verbose_name_plural': '远程主机用户',
                'verbose_name': '远程主机用户',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=1)),
                ('memo', models.TextField(blank=1, null=1)),
            ],
            options={
                'verbose_name_plural': '数据中心',
                'verbose_name': '数据中心',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('task_type', models.CharField(choices=[('multi_cmd', 'CMD'), ('file_send', '批量发送文件'), ('file_get', '批量下载文件')], max_length=50)),
                ('cmd', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('task_pid', models.IntegerField(default=0)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('hosts', models.ManyToManyField(to='hosts.BindHostToUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '批量任务',
                'verbose_name': '批量任务',
            },
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('unknown', 'Unknown')], default='unknown', max_length=30)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('bind_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.BindHostToUser')),
                ('child_of_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.TaskLog')),
            ],
            options={
                'verbose_name_plural': '批量任务日志',
                'verbose_name': '批量任务日志',
            },
        ),
        migrations.AlterUniqueTogether(
            name='hostuser',
            unique_together=set([('auth_type', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.IDC'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.Host'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host_groups',
            field=models.ManyToManyField(to='hosts.HostGroup'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.HostUser'),
        ),
        migrations.AlterUniqueTogether(
            name='host',
            unique_together=set([('ip_address', 'port')]),
        ),
        migrations.AlterUniqueTogether(
            name='bindhosttouser',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
