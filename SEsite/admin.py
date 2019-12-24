from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','password','name','profile','work','phone','createTime',
                    'isVerificated','isFreezed')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name','code','describe','creator','buildTime','lastUpdateTime','memberNum')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','name','nameProject','code','content','editTime','pushTime','deadLine','isPushed')

class ApplyAdmin(admin.ModelAdmin):
    list_display = ('id','userEmail','userName','projectCode','instruction','result','check')

class InviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'userEmail', 'projectCode', 'instruction', 'result','check')

class MsgAdmin(admin.ModelAdmin):
    list_display = ('id','userId','projectId','content','fromWho','pushTime','isSend')

class RepoAdmin(admin.ModelAdmin):
    list_display = ('id','userId','file')

class CommitAdmin(admin.ModelAdmin):
    list_display = ('id','taskId','userId','username','name','content','file','commitTime')

admin.site.register(User,UserAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Apply,ApplyAdmin)
admin.site.register(Invite,InviteAdmin)
admin.site.register(Message, MsgAdmin)
admin.site.register(Repository,RepoAdmin)
admin.site.register(Commit,CommitAdmin)