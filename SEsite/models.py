from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):
    id=models.AutoField('id',primary_key=True)                  # 编号
    email=models.EmailField('email')                            # 邮箱
    password=models.CharField('password',max_length=16)         # 密码
    name=models.CharField('name',max_length=12)                 # 姓名
    profile=models.TextField('profile',default='')              # 简介
    work=models.CharField('work',max_length=12)                 # 工作
    phone=models.CharField('phone',max_length=11)               # 手机
    createTime=models.DateField('creaetTime',auto_now_add=True)   # 创建时间
    isVerificated=models.BooleanField('isVerificated',default=False)          # 是否验证
    isFreezed=models.BooleanField('isFreezed',default=False)                  # 是否冻结

    projectInCharge=models.ManyToManyField('Project',through='shipUserProject',
                                           through_fields=('user','project'))   # 负责的项目
    taskInCharge=models.ManyToManyField('Task',through='shipUserTask',
                                        through_fields=('user','task'))         # 负责的任务

class Project(models.Model):
    id=models.AutoField('id',primary_key=True)                  # 编号
    name=models.CharField('name',max_length=12)                 # 名称
    code=models.CharField('code',max_length=12)                 # 代码，仅允许字母开头，且仅允许含有字母和数字，唯一
    describe=models.CharField('describe',max_length=140)        # 描述
    creator = models.EmailField('email',default='')  # 邮箱

    buildTime=models.DateField('buildTime',auto_now_add=True)   # 创建时间
    lastUpdateTime=models.DateField('lastUpdateTime',auto_now=True) # 上次更新时间
    memberNum=models.IntegerField('memberNum')                  # 成员个数

    member=models.ManyToManyField('User',through='shipUserProject',
                                  through_fields=('project','user'))    # 成员关系
    task=models.ManyToManyField('Task',through='shipProjectTask',
                                through_fields=('project','task'))      # 任务关系


class Task(models.Model):
    id=models.AutoField('id',primary_key=True)                  # 编号
    name=models.CharField('name',max_length=12)                 # 任务名字
    nameProject=models.CharField('name',max_length=12,default='')                 # 项目名字
    code=models.CharField('code',max_length=12,default='')                 # 代码，仅允许字母开头，且仅允许含有字母和数字，唯一
    content=models.TextField('content')                         # 内容
    editTime=models.DateField('editTime',auto_now_add=True)     # 编辑时间
    pushTime=models.DateField('pushTime',auto_now_add=True)                       # 推送时间
    deadLine=models.DateField('deadLine')                       # 截止时间
    isPushed=models.BooleanField('isPushed',default=False)

    member=models.ManyToManyField('User',through='shipUserTask',
                                  through_fields=('task','user'))   # 隶属该任务的成员

class Apply(models.Model):
    id = models.AutoField('id', primary_key=True)               # 编号
    userEmail=models.EmailField('email')                        # 邮箱
    userName=models.CharField('userName',max_length=12)
    projectCode=models.CharField('code',max_length=12)                        # 项目代码
    instruction=models.CharField('instruction',max_length=140)  # 申请说明
    result=models.BooleanField('result',default=False)                        # 申请结果
    check=models.BooleanField('check',default=False)

class Invite(models.Model):
    id = models.AutoField('id', primary_key=True)                   # 编号
    projectCode = models.CharField('code',max_length=12)  # 项目代码
    userEmail = models.EmailField('email')                          # 邮箱
    instruction = models.CharField('instruction', max_length=140)  # 邀请说明
    result = models.BooleanField('result',default=False)  # 邀请结果
    check=models.BooleanField('check',default=False)

class Commit(models.Model):
    id=models.AutoField('id',primary_key=True)                  # 编号
    taskId=models.IntegerField('taskId')
    userId=models.IntegerField('userId',default=0)
    username=models.CharField('name',max_length=12,default='')                 # 名字
    name=models.CharField('name',max_length=12)                 # 任务名字
    content=models.TextField('content')                         # 内容
    file=models.FileField('file',upload_to='commit/')
    commitTime = models.DateField('commitTime', default=timezone.now)  # 创建时间

class shipUserProject(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)

class shipUserTask(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    task=models.ForeignKey(Task,on_delete=models.CASCADE)

class shipProjectTask(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    task=models.ForeignKey(Task,on_delete=models.CASCADE)


class Message(models.Model):
    id=models.AutoField('id', primary_key=True)                   # 编号
    isUser=models.BooleanField('isUser',default=True)
    userId=models.IntegerField('userId')
    projectId = models.IntegerField('projectId')
    content=models.TextField('content')
    fromWho = models.CharField('fromWho',max_length=12)
    pushTime=models.DateField('pushTime',auto_now_add=True)
    isSend=models.BooleanField('isSend',default=False)

class Repository(models.Model):
    id=models.AutoField('id', primary_key=True)                   # 编号
    isUser=models.BooleanField('isUser',default=True)
    userId = models.IntegerField('userId',default=0)
    projectId = models.IntegerField('projectId',default=0)
    name=models.CharField('name',max_length=120,default='null')
    file=models.FileField('file',upload_to='file/')