from django.db import models
from hosts.cus_auth import UserProfile
# Create your models here.


class Host(models.Model):
    name = models.CharField(max_length=64)
    sn = models.CharField(max_length=128)
    # 此处sn不加非空约束是因为hostbiao可以包含虚拟机，我们cmdb中的server也不能直接外键关联到host表，后续可以通过第三方脚本来实现数据导入
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField(default=22)
    idc = models.ForeignKey('IDC')
    system_type_choices = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
    )
    system_type = models.CharField(choices=system_type_choices, max_length=32, default='linux')
    enabled = models.BooleanField(default=1)
    memo = models.TextField(blank=1, null=1)
    date = models.DateTimeField(auto_now_add=1)

    def __str__(self):
        return "%s(%s)" % (self.name, self.ip_address)

    class Meta:
        unique_together = ('ip_address', 'port')
        # 联合唯一约束，要考虑虚拟机的情况
        verbose_name = u'远程主机'
        verbose_name_plural = u"远程主机"


class IDC(models.Model):
    name = models.CharField(max_length=64, unique=1)
    memo = models.TextField(blank=1, null=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'数据中心'
        verbose_name_plural = u"数据中心"


class HostUser(models.Model):
    auth_type_choices = (
        ('ssh-password', 'SSH/PASSWORD'),
        ('ssh-key', 'SSH/KEY'),
    )
    auth_type = models.CharField(choices=auth_type_choices, max_length=32, default='ssh-password')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=1, null=1)

    def __str__(self):
        return "(%s)%s" % (self.auth_type, self.username)

    class Meta:
        unique_together = ('auth_type', 'username', 'password')
        verbose_name = u'远程主机用户'
        verbose_name_plural = u"远程主机用户"


class HostGroup(models.Model):
    name = models.CharField(unique=1, max_length=64)
    memo = models.TextField(blank=1, null=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u"主机组"


class BindHostToUser(models.Model):
    host = models.ForeignKey("Host")
    host_user = models.ForeignKey("HostUser")
    # host_user= models.ManyToManyField("HostUser")
    host_groups = models.ManyToManyField("HostGroup")

    class Meta:
        unique_together = ('host', 'host_user')
        verbose_name = u'主机与用户绑定关系'
        verbose_name_plural = u"主机与用户绑定关系"

    def __str__(self):
        return '%s:%s' % (self.host.name, self.host_user.username)

    def get_groups(self):
        return ','.join([g.name for g in self.host_groups.select_related()])


class TaskLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    task_type_choices = (('multi_cmd', "CMD"), ('file_send', "批量发送文件"), ('file_get', "批量下载文件"))
    task_type = models.CharField(choices=task_type_choices, max_length=50)
    user = models.ForeignKey('UserProfile')
    hosts = models.ManyToManyField('BindHostToUser')
    cmd = models.TextField()
    expire_time = models.IntegerField(default=30)
    task_pid = models.IntegerField(default=0)   # master process pid
    note = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "task_id:%s cmd:%s" % (self.id, self.cmd)

    class Meta:
        verbose_name = u'批量任务'
        verbose_name_plural = u'批量任务'


class TaskLogDetail(models.Model):
    child_of_task = models.ForeignKey('TaskLog')
    bind_host = models.ForeignKey('BindHostToUser')
    date = models.DateTimeField(auto_now_add=True)  # finished date
    event_log = models.TextField()
    result_choices = (('success', 'Success'), ('failed', 'Failed'), ('unknown', 'Unknown'))
    result = models.CharField(choices=result_choices, max_length=30, default='unknown')
    note = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "child of:%s result:%s" %(self.child_of_task.id, self.result)

    class Meta:
        verbose_name = u'批量任务日志'
        verbose_name_plural = u'批量任务日志'
