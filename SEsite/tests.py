import unittest
from .models import *
from .base import *
from .forms import *

# Create your tests here.

class UserTest(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.user = User.objects.create(email='test@qq.com', name='test', phone='12345678901',
                                   work='test', password='password', profile='profile',
                                   isVerificated=True, isFreezed=False)
        self.user2 = User.objects.create(email='test2@qq.com', name='test2', phone='12345678901',
                                   work='test', password='password', profile='profile',
                                   isVerificated=True, isFreezed=False)
        self.project=Project.objects.create(name='testProject',code='testCode',describe='test',
                                       creator='test@qq.com',memberNum=1)
        self.task=Task.objects.create(name='testTask',nameProject='testProject',code='testCode',content='testTask',isPushed=True)
        self.apply=Apply.objects.create(userEmail='test2@qq.com',userName='test2',projectCode='testCode',instruction='test apply')
        self.invite=Invite.objects.create(projectCode='testCode',userEmail='test2@qq.com',instruction='test invite')
        # self.commit=Commit.objects.create(taskId=self.task.id,userId=self.user.id,username=self.user.name,content='test commit')
        self.message=Message.objects.create(userId=self.user.id,projectId=0,content='test message',fromWho='Admin')
        #self.repository=Repository.objects.create(userId=self.user.id)

    def test_editPassword(self):
        ControlUser.editPassword(nowPassword=self.user.password,toChange='changed',id=self.user.id)
        str=User.objects.get(id=self.user.id).password
        self.assertEqual('changed',str)
        return

    def test_deleteUser(self):
        user = User.objects.create(email='test3@qq.com', name='test3', phone='12345678901',
                                   work='test', password='password', profile='profile',
                                   isVerificated=True, isFreezed=False)
        id=user.id
        ControlUser.deleteUser(id=user.id,password=user.password)
        self.assertEqual(False,User.objects.filter(id=id).exists())
        return

    def test_joinProject(self):
        ControlUser.joinProject(id=self.user.id,code=self.project.code,instruction='test')
        self.assertEqual(True,Apply.objects.filter(userEmail=self.user.email,projectCode=self.project.code).exists())
        Apply.objects.get(userEmail=self.user.email,projectCode=self.project.code).delete()
        return

    def test_decideInvitation(self):
        ControlUser.decideInvitation(id=self.invite.id,userId=self.user.id,decision=True)
        self.assertEqual(True,Invite.objects.get(id=self.invite.id).check)
        self.assertEqual(True,self.user.projectInCharge.filter(code=self.project.code).exists())
        self.assertEqual(True,self.project.member.filter(id=self.user.id).exists())
        return

    def test_editProject(self):
        ControlProject.editProject(id=self.project.id,describe='test new describe',name='test new name')
        tmp=Project.objects.get(id=self.project.id)
        self.assertEqual('test new describe',tmp.describe)
        self.assertEqual('test new name',tmp.name)
        return

    def test_checkApply(self):
        ControlProject.checkApply(id=self.apply.id,decision=True)
        self.assertEqual(True,Apply.objects.get(id=self.apply.id).check)
        self.assertEqual(True,self.user2.projectInCharge.filter(code=self.project.code).exists())
        self.assertEqual(True,self.project.member.filter(id=self.user2.id).exists())
        return

    def test_inviteUser(self):
        ControlProject.inviteUser(email='test3@qq.com',code=self.project.code,instruction='test ins')
        self.assertEqual('test3@qq.com',Invite.objects.get(projectCode=self.project.code,instruction='test ins').userEmail)
        Invite.objects.get(projectCode=self.project.code, instruction='test ins').delete()
        return

    def test_deleteMember(self):
        ControlProject.deleteMember(email='test2@qq.com',code=self.project.code,reason='test')
        self.assertEqual(False,self.project.member.filter(email='test2@qq.com').exists())

    def test_commitTask(self):
        ControlTask.commitTask(taskId=self.task.id,userId=self.user.id,name=self.user.name,content='test commit')
        self.assertEqual(True,Commit.objects.filter(taskId=self.task.id,userId=self.user.id).exists())
        self.assertEqual('test commit',Commit.objects.get(taskId=self.task.id).content)
        Commit.objects.get(taskId=self.task.id).delete()
        return

    def test_sendMsg(self):
        ControlMsg.sendMsg(userId=self.user.id,projectId=0,fromWho='admin',content='test2')
        self.assertEqual(True,Message.objects.filter(userId=self.user.id,content='test2').exists())
        Message.objects.get(content='test2').delete()
        return

    def test_deleteMsg(self):
        id=self.message.id
        ControlMsg.deleteMsg(id=self.message.id)
        self.assertEqual(False,Message.objects.filter(id=id).exists())

    def test_deleteProject(self):
        project = Project.objects.create(name='testProject2', code='testCode2', describe='test',
                                              creator='test@qq.com', memberNum=1)
        id=project.id
        ControlProject.deleteProject(id=self.user.id,code=project.code,password=self.user.password)
        self.assertEqual(False,Project.objects.filter(id=id).exists())
        return

    @classmethod
    def tearDownClass(self):
        self.user.delete()
        self.user2.delete()
        self.project.delete()
        self.task.delete()
        self.apply.delete()
        self.invite.delete()
        #self.commit.delete()
        #self.message.delete()
        #self.repository.delete()
