from django.http import HttpResponse
from django.http import request

from django import forms
import django.utils.timezone as timezone
from captcha.models import CaptchaStore
from captcha.helpers import  captcha_image_url
import json

from .forms import *
from .models import *


# 创建验证码
def createCaptcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha

# 验证验证码
def checkCaptcha(request):
    return True
    captchaStr = request.POST.get("captcha", None)  # 用户提交的验证码
    captchaHashkey = request.POST.get("hashkey", None)  # 验证码答案
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
                return True
        except:
            return False
    else:
        return False

# 检查用户或者项目是否存在
def checkExist(id='',email='',code='',model=User):
    if id!='':
        return model.objects.filter(id=id).exists()
    if email!='':
        return model.objects.filter(email=email).exists()
    if code!='':
        return model.objects.filter(code=code).exists()
    return False

class ControlUser:
    # 登录验证
    @staticmethod
    def checkSignIn(form=FormSignIn()):
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        if checkExist(email=email,model=User):
            user=User.objects.get(email=email)
            if password==user.password:
                if user.isVerificated==True and user.isFreezed==False:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # 注册用户
    @staticmethod
    def register(form=FormSignUp):
        email = form.cleaned_data['email']
        name=form.cleaned_data['name']
        phone=form.cleaned_data['phone']
        work=form.cleaned_data['work']
        password = form.cleaned_data['password']
        profile=form.cleaned_data['profile']
        isVerificated=True
        isFreezed=False
        if checkExist(email=email):
            return False
        else:
            user=User.objects.create(email=email,name=name,phone=phone,
                                work=work,password=password,profile=profile,isVerificated=isVerificated,
                                isFreezed=isFreezed)
            str='欢迎使用项目管理系统！'+user.name
            ControlMsg.sendMsg(userId=user.id,fromWho='admin',content=str)
            return True

    # 编辑用户信息
    @staticmethod
    def editUserInfo(form=FormEditUser(),id=0):
        user=User.objects.get(id=id)
        user.name = form.cleaned_data['name']
        user.phone = form.cleaned_data['phone']
        user.work = form.cleaned_data['work']
        user.profile=form.cleaned_data['profile']
        user.save()
        str = user.name+': 您已成功修改自身的用户信息!'
        ControlMsg.sendMsg(userId=user.id, fromWho='admin', content=str)
        return


    # 修改密码
    @staticmethod
    def editPassword(nowPassword='',toChange='',id=''):
        user=User.objects.get(id=id)
        if user.password==nowPassword:
            user.password=toChange
            user.save()
            str = user.name + ': 您已成功修改密码！'
            ControlMsg.sendMsg(userId=user.id, fromWho='admin', content=str)
            return True
        else:
            return False

    # 注销用户
    @staticmethod
    def deleteUser(id=0,password=''):
        user=User.objects.get(id=id)
        if user.password==password:
            user.delete()
            return True
        else:
            return False

    # 申请项目
    @staticmethod
    def joinProject(id=0,code='',instruction=''):
        user = User.objects.get(id=id)
        Apply.objects.create(userEmail=user.email,projectCode=code,instruction=instruction)
        return

    # 决定邀请结果
    @staticmethod
    def decideInvitation(id='',userId='',decision=False):
        tmp=Invite.objects.get(id=id)
        tmp.result=decision
        if decision:
            user=User.objects.get(id=userId)
            project=Project.objects.get(code=tmp.projectCode)
            user.projectInCharge.add(project)
            project.member.add(user)
        tmp.check=True
        tmp.save()

class ControlProject:
    # 创建项目
    @staticmethod
    def createProject(form=FormCreateProject(),id=0):
        user=User.objects.get(id=id)
        name=form.cleaned_data['name']
        code=form.cleaned_data['code']
        print(code)
        describe=form.cleaned_data['describe']
        if checkExist(code=code,model=Project):
            return False
        else:
            project=Project.objects.create(name=name,code=code,creator=user.email,describe=describe,memberNum=1)
            user.projectInCharge.add(project)
            return True

    @staticmethod
    def editProject(name='',describe='',id=''):
        project=Project.objects.get(id=id)
        project.name=name
        project.describe=describe
        project.save()

    @staticmethod
    def deleteProject(id='',code='',password=''):
        project=Project.objects.get(code=code)
        user=User.objects.get(id=id)
        if project.creator==user.email and user.password==password:
            project.delete()
            return True
        else:
            return False

    # 审核申请
    @staticmethod
    def checkApply(id='',decision=False):
        tmp = Apply.objects.get(id=id)
        tmp.result = decision
        if decision:
            project=Project.objects.get(code=tmp.projectCode)
            project.member.add(User.objects.get(email=tmp.userEmail))
            project.memberNum+=1
            project.save()
        tmp.check=True
        tmp.save()

    # 邀请成员
    @staticmethod
    def inviteUser(email='',code='',instruction=''):
        Invite.objects.create(userEmail=email,projectCode=code,instruction=instruction)

    @staticmethod
    def deleteMember(email='',code='',reason=''):
        tmp=Project.objects.get(code=code).member
        ControlMsg.sendMsg(userId=User.objects.get(email=email).id,fromWho=Project.objects.get(code=code).name,content=reason)
        tmp.remove(User.objects.get(email=email))


class ControlTask:
    @staticmethod
    def createTask(form=FormCreateTask(),code=''):
        name=form.cleaned_data['name']
        content=form.cleaned_data['content']
        # pushTime=form.cleaned_data['pushTime']
        deadLine=form.cleaned_data['deadLine']
        member=form.cleaned_data['member']
        result = (re.match(r'^(.+@.+\..+,)*(.+@.+\..+)+', member).span())
        if result == None or member[-1] == ',':
            return False
        print(member)
        task=Task.objects.create(name=name,content=content,nameProject=Project.objects.get(code=code).name,code=code,deadLine=deadLine,isPushed=True)
        member=member.split(',')
        print(member)
        for one in member:
            task.member.add(User.objects.get(email=one))
        member = task.member.all()
        content = "你获得了一个新的任务：" + task.name
        for one in member:
            ControlMsg.sendMsg(userId=one.id, fromWho=Project.objects.get(code=code).name, content=content)
        return True

    @staticmethod
    def commitTask(taskId='', userId='', name='', content='', file=''):
        username=User.objects.get(id=userId).name
        if file=='':
            Commit.objects.create(taskId=taskId, userId=userId,username=username,name=name,content=content)
        else:
            Commit.objects.create(taskId=taskId, userId=userId, username=username,name=name, content=content,file=file)


class ControlMsg:
    @staticmethod
    def sendMsg(userId=0, projectId=0, fromWho='', pushTime='now', content=''):
        msg=Message.objects.create(userId=userId,projectId=projectId,fromWho=fromWho,content=content)
        if userId!='':
            msg.isUser=True
        if projectId!='':
            msg.isUser=False

        if pushTime=='now':
            msg.isSend=True
        else:
            msg.pushTime=pushTime
            msg.isSend=False
        msg.save()
        
    @staticmethod
    def deleteMsg(id=''):
        msg=Message.objects.get(id=id)
        msg.delete()


class ControlFile:
    @staticmethod
    def uploadFile(file,id='',pid=''):
        if id!='':
            c=Repository.objects.create(userId=id,file=file)
            print(c.file.name)
            print(c.file.size)
            return True
        if pid!='':
            Repository.objects.create(projectId=pid,file=file)
            return True

    @staticmethod
    def deleteFile(id=''):
        file=Repository.objects.get(id=id)
        file.delete()








