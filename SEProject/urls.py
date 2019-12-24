"""SEProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import url
from SEsite import views

urlpatterns = [
    url(r'^$', views.SignIn),           # 根目录
    url(r'signIn/', views.SignIn),  # 登录
    url(r'signUp/', views.SignUp),  # 注册
    url(r'signOut/', views.SignOut),  # 登出
    url(r'index/', views.Index),  # 主页面
    url(r'admin/', admin.site.urls),  # 管理
    url(r'captcha/', include('captcha.urls')),  # 图片验证码

    url(r'info-edit/', views.InfoEdit),
    url(r'info-project-deal/', views.InfoProjectDeal),
    url(r'info-pwd/', views.PwdEdit),
    url(r'info-delete/', views.DeleteUser),


    url(r'm-p-info/', views.MPInfo),
    url(r'm-create/', views.MCreate),
    url(r'm-add-user/', views.MAddUser),
    url(r'm-del-user/', views.MDelUser),
    url(r'm-add-task/', views.MAddTask),
    url(r'm-commit-task/', views.MCommitTask),
    url(r'm-sendmsg/', views.MSendMsg),
    url(r'm-edit/', views.MEdit),
    url(r'manage/', views.Manage),

    url(r'info/', views.Info),
    url(r'msg-sendmsg/', views.MsgSendMsg),
    url(r'msg/', views.Msg),

    url(r'task/', views.Tasks),
    url(r'file/', views.File),

    path('test',views.MakeTest),


]
