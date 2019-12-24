from django.shortcuts import render
from django.http import *
from django.http import request
from django.http import StreamingHttpResponse

from captcha.models import CaptchaStore
from captcha.helpers import  captcha_image_url

from .base import *
from .forms import *
from .models import *

# 重定向

def rSignIn(request):
    return HttpResponseRedirect('../signIn/')

def rSignOut(request):
    return HttpResponseRedirect('../signOut/')

def rSignUp(request):
    return HttpResponseRedirect('../signUp/')

def rIndex(request):
    return HttpResponseRedirect('../index/')

def rInfo(request):
    return HttpResponseRedirect('info/')

def rManage(request):
    return HttpResponseRedirect('manage/')

def rMsg(request):
    return HttpResponseRedirect('msg/')

def rTask(request):
    return HttpResponseRedirect('task/')

def rFile(request):
    return HttpResponseRedirect('file/')

# 登录
def SignIn(request):
    '''
    status:
        status 1 验证码错误
        status 2 表单错误
        status 3 用户名或密码错误
        status 4 修改成功
    '''
    if request.method=='GET':
        form=FormSignIn()
        captcha=createCaptcha()
        return render(request,'sign-in.html',locals())
    if request.method=='POST':
        form=FormSignIn(request.POST)
        status = 0
        if checkCaptcha(request):
            if form.is_valid():
                if ControlUser.checkSignIn(form):
                    request.session['id']=User.objects.get(email=form.cleaned_data['email']).id
                    return HttpResponseRedirect('../index/')
                else:
                    status=3
            else:
                status=2
        else:
            status=1
        form = FormSignIn()
        captcha = createCaptcha()
        return render(request,'sign-in.html',locals())

# 注册
def SignUp(request):
    '''
    status:
        status 1 验证码错误
        status 2 表单错误
    '''
    if request.method=='GET':
        form=FormSignUp()
        captcha=createCaptcha()
        return render(request,'sign-up.html',locals())
    if request.method=='POST':
        form=FormSignUp(request.POST)
        status = {}
        if checkCaptcha(request):
            if form.is_valid():
                ControlUser.register(form)
                return HttpResponseRedirect('/signIn/')
            else:
                status=2
        else:
            status=1
        form = FormSignUp()
        captcha = createCaptcha()
        return render(request, 'sign-up.html', locals())

# 登出
def SignOut(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

# 主页
def Index(request):
    if request.method=='GET':
        user=User.objects.get(id=request.session['id'])
        msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
        msg=msgAll
        if len(msgAll)>3:
            msg=msgAll[0:3]
        task=user.taskInCharge.filter(isPushed=True)
        if len(task)>3:
            task=task[0:3]
        return render(request,'index.html',locals())

# 个人界面
def Info(request):
    '''
    tool 0 个人界面
    tool 1 修改信息
    tool 2 修改邮箱
    tool 3 修改密码
    tool 4 注销用户
    :param request:
    :return:
    '''
    if request.method == 'GET':
        user = User.objects.get(id=request.session['id'])
        msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
        msg=msgAll
        if len(msgAll) > 3:
            msg = msgAll[0:3]
        task = user.taskInCharge.filter(isPushed=True)
        if len(task) > 3:
            task = task[0:3]
        tool=0
        return render(request,'info/info.html',locals())

def InfoEdit(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.session['id'])
        msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
        msg=msgAll
        if len(msgAll) > 3:
            msg = msgAll[0:3]
        task = user.taskInCharge.filter(isPushed=True)
        if len(task) > 3:
            task = task[0:3]
        form=FormEditUser()
        tool=1
        return render(request,'info/edit.html',locals())
    if request.method=='POST':
        form = FormEditUser(request.POST)
        status=0
        if checkCaptcha(request):
            if form.is_valid():
                ControlUser.editUserInfo(form,id=request.session['id'])
                return HttpResponseRedirect('info')
            else:
                status=1
        else:
            status=2
        form = FormEditUser()
        return render(request, 'info/edit.html', locals())

def InfoProjectDeal(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool = 2
    status=0
    invite=Invite.objects.filter(userEmail=user.email,check=False)
    if request.method == 'GET':
        return render(request,'info/project-deal.html',locals())
    if request.method=='POST':
        code=request.POST.get('code','')
        instruction=request.POST.get('instruction','')
        accept=request.POST.get('accept','')
        reject=request.POST.get('reject','')
        if accept!='':
            ControlUser.decideInvitation(id=accept,userId=user.id,decision=True)
            return render(request,'info/info.html',locals())
        if reject!='':
            ControlUser.decideInvitation(id=reject,userId=user.id, decision=False)
            return render(request, 'info/info.html', locals())
        if code!='':
            if Project.objects.filter(code=code).exists():
                ControlUser.joinProject(id=user.id,instruction=instruction,code=code)
                status=6
                return render(request, 'info/info.html', locals())
            else:
                status=5
                return render(request,'info/project-deal.html',locals())



def PwdEdit(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    form = FormEditUser()
    tool = 3
    if request.method == 'GET':
        return render(request,'info/pwd.html',locals())
    if request.method=='POST':
        nowPassword=request.POST.get('nowPassword')
        toChange=request.POST.get('toChange')
        checkToChange=request.POST.get('checkToChange')
        if toChange!=checkToChange:
            status=2
            return render(request, 'info/pwd.html', locals())
        else:
            if ControlUser.editPassword(nowPassword,toChange,id=request.session['id']):
                del request.session['id']
                status=4
                form=FormSignIn()
                return HttpResponseRedirect('signIn/')
            else:
                status=3
                return render(request,'info/pwd.html',locals())


def DeleteUser(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool = 4
    if request.method == 'GET':
        return render(request, 'info/delete.html', locals())
    if request.method == 'POST':
        password=request.POST.get('password')
        code=request.POST.get('code')
        if ControlUser.deleteUser(id=request.session['id'],password=password):
            del request.session['id']
            status=4
            form = FormSignIn()
            return render(request,'sign-in.html',locals())
        else:
            status=4
            return render(request,'info/delete.html',locals())

def Manage(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    if request.method=='GET':
        project = user.projectInCharge.all()
        projectNum=len(project)
        return render(request,'manage/manage.html',locals())
    if request.method=='POST':
        code=request.POST.get('code')
        request.session['pid']=Project.objects.get(code=code).id
        project=Project.objects.get(code=code)
        member=project.member.all()
        tool=0
        return render(request,'manage/p-info.html',locals())



def MCreate(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    if request.method=='GET':
        form=FormCreateProject()
        captcha=createCaptcha()
        return render(request,'manage/create.html',locals())
    if request.method=='POST':
        form=FormCreateProject(request.POST)
        if checkCaptcha(request):
            if form.is_valid():
                ControlProject.createProject(form,id=request.session['id'])
                request.session['pid']=Project.objects.get(code=form.cleaned_data['code']).id
                return render(request,'/manage/p-info',locals())
            else:
                status=1
        else:
            status=2
        form = FormCreateProject()
        captcha = createCaptcha()
        return render(request, 'manage/create.html', locals())

def MPInfo(request):
    user = User.objects.get(id=request.session['id'])
    project=Project.objects.get(id=request.session['pid'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=0
    if request.method=='GET':
        project = Project.objects.get(id=request.session['pid'])
        member = project.member.all()
        return render(request, 'manage/p-info.html', locals())

def MAddUser(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=1
    status = 0
    project = Project.objects.get(id=request.session['pid'])
    apply=Apply.objects.filter(projectCode=project.code,check=False)
    if request.method=='GET':
        project = Project.objects.get(id=request.session['pid'])
        return render(request, 'manage/add-user.html', locals())
    if request.method=='POST':
        email = request.POST.get('email', '')
        instruction = request.POST.get('instruction', '')
        accept = request.POST.get('accept', '')
        reject = request.POST.get('reject', '')
        if accept != '':
            ControlProject.checkApply(id=accept,decision=True)
            status=9
            return HttpResponseRedirect('p-info',locals())
        if reject != '':
            status=9
            ControlUser.decideInvitation(id=reject, userId=user.id, decision=False)
            return HttpResponseRedirect('p-info',locals())
        if email!='':
            if checkExist(email=email):
                if not project.member.filter(email=email).exists():
                    ControlProject.inviteUser(email=email,code=Project.objects.get(id=request.session['pid']).code,instruction=instruction)
                    status=6
                    return render(request,'manage/p-info.html',locals())
                else:
                    status=5
            else:
                status=4
        else:
            status=3
        project = Project.objects.get(id=request.session['pid'])
        return render(request, 'manage/add-user.html', locals())




def MDelUser(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=2
    project = Project.objects.get(id=request.session['pid'])
    status=0
    if request.method=='GET':
        return render(request,'manage/del-user.html',locals())
    if request.method=='POST':
        email=request.POST.get('email','')
        reason=request.POST.get('reason','')
        if email!='' and User.objects.filter(email=email).exists():
            ControlProject.deleteMember(email=email,code=project.code,reason=reason)
            status=9
            return render(request,'manage/p-info.html',locals())
        else:
            status=3
            return render(request,'manage/del-user.html',locals())


def MAddTask(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=3
    project = Project.objects.get(id=request.session['pid'])
    status = 0
    if request.method=='GET':
        form=FormCreateTask()
        return render(request,'manage/add-task.html',locals())
    if request.method=='POST':
        form = FormCreateTask(request.POST)
        if form.is_valid():
            if ControlTask.createTask(form,code=project.code):
                status=11
                return HttpResponseRedirect('../m-commit-task',locals())
            else:
                status=1
                return render(request, 'manage/add-task.html', locals())
        else:
            status=1
            return render(request,'manage/add-task.html',locals())


class nodeC:
    task=None
    upload=None

def MCommitTask(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    project = Project.objects.get(id=request.session['pid'])
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    taskAll = Task.objects.filter(isPushed=True, code=project.code)
    if len(taskAll) > 3:
        task = taskAll[0:3]
    tool=4
    commit=[]
    for one in taskAll:
        a =nodeC()
        a.task=one
        c=Commit.objects.filter(taskId=one.id)
        a.upload=c
        commit.append(a)
    if request.method=='GET':
        return render(request,'manage/commit-task.html',locals())
    if request.method=='POST':
        delete = request.POST.get('delete', '')
        download = request.POST.get('download', '')
        if delete != '':
            Commit.objects.get(id=download).delete()
            status = 9
            return render(request, 'file/file.html', locals())
        if download != '':
            file = Commit.objects.get(id=download).file
            response = StreamingHttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            str = 'attachment;filename="{0}"'.format(file.name).encode('utf-8')
            str = str[5:]
            response['Content-Disposition'] = str
            return response
        file = request.FILES.get('upload', '')
        if file != '':
            if ControlFile.uploadFile(file, id=user.id):
                status = 2
                return render(request, 'file/file.html', locals())

def MSendMsg(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=5
    project = Project.objects.get(id=request.session['pid'])
    status=0
    if request.method=='GET':
        return render(request,'manage/send-msg.html',locals())
    if request.method=='POST':
        email = request.POST.get('email', '')
        content = request.POST.get('content', '')
        if email!='' and User.objects.filter(email=email).exists():
            ControlMsg.sendMsg(userId=User.objects.get(email=email).id,fromWho=project.name,content=content)
            status=8
            return render(request,'manage/p-info.html',locals())
        else:
            status=4
            return render(request,'manage/send-msg.html',locals())



def MEdit(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=6
    status=0
    project = Project.objects.get(id=request.session['pid'])
    if request.method=='GET':
        return render(request,'manage/edit.html',locals())
    if request.method=='POST':
        name=request.POST.get('name','')
        describe=request.POST.get('describe','')
        password=request.POST.get('password','')
        if password=='':
            if name!='' and describe!='':
                ControlProject.editProject(name=name,describe=describe,id=request.session['pid'])
                status=9
                return render(request,'manage/p-info.html',locals())
            else:
                status=1
                return render(request,'manage/edit.html',locals())
        else:
            if ControlProject.deleteProject(id=user.id,code=project.code,password=password):
                return HttpResponseRedirect('index/',locals())
            else:
                status=10
                return render(request,'manage/edit.html',locals())




def Msg(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    else:
        msg = msgAll
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    if request.method=='GET':
        return render(request,'msg/msg.html',locals())
    if request.method=='POST':
        id=request.POST.get('delete','')
        ControlMsg.deleteMsg(id)
        return HttpResponseRedirect('msg',locals())


def Tasks(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    taskAll = user.taskInCharge.filter(isPushed=True)
    if len(taskAll) > 3:
        task = taskAll[0:3]
    lenTask=0
    if len(taskAll)==0:
        lenTask=1
    if request.method=='GET':
        return render(request,'task/task.html',locals())
    if request.method=='POST':
        name=request.POST.get('name','')
        content=request.POST.get('content','')
        file=request.FILES.get('upload','')
        taskId=request.POST.get('taskId','')
        ControlTask.commitTask(taskId=taskId,userId=user.id,name=name,content=content,file=file)
        return render(request,'task/task.html',locals())

def MsgSendMsg(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=5
    project = Project.objects.get(id=request.session['pid'])
    status=0
    if request.method=='GET':
        return render(request,'msg/send-msg.html',locals())
    if request.method=='POST':
        email = request.POST.get('email', '')
        content = request.POST.get('content', '')
        if email!='' and User.objects.filter(email=email).exists():
            ControlMsg.sendMsg(userId=User.objects.get(email=email).id,fromWho=user.name,content=content)
            status=1
            return render(request,'msg/send-msg.html',locals())
        else:
            status=2
            return render(request,'msg/send-msg.html',locals())

def File(request):
    user = User.objects.get(id=request.session['id'])
    msgAll = Message.objects.filter(userId=user.id, isSend=True).order_by('-id')
    msg=msgAll
    if len(msgAll) > 3:
        msg = msgAll[0:3]
    else:
        msg = msgAll
    task = user.taskInCharge.filter(isPushed=True)
    if len(task) > 3:
        task = task[0:3]
    tool=0
    status=0
    files=Repository.objects.filter(userId=user.id)
    if request.method == 'GET':
        files = Repository.objects.filter(userId=user.id)
        return render(request, 'file/file.html', locals())
    if request.method=='POST':
        delete=request.POST.get('delete','')
        download=request.POST.get('download','')
        if delete!='':
            ControlFile.deleteFile(delete)
            status=3
            return render(request,'file/file.html',locals())
        if download!='':
            file=Repository.objects.get(id=download).file
            response = StreamingHttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            str='attachment;filename="{0}"'.format(file.name).encode('utf-8')
            str=str[5:]
            response['Content-Disposition'] = str
            return response
        file=request.FILES.get('upload','')
        if file!='':
            if ControlFile.uploadFile(file,id=user.id):
                status=2
                return render(request,'file/file.html',locals())

def MakeTest(request):
    if request.method == 'GET':
        Project.objects.get(id=5).member.add(User.objects.get(id=3))
        User.objects.get(id=3).projectInCharge.add(Project.objects.get(id=5))
        return HttpResponse('Finished')


