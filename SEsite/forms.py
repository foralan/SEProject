from django import forms
from django.forms import ValidationError
from .models import *
import re

class FormSignIn(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'form-control'}
    ))
    password=forms.CharField(min_length=6,max_length=18,widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ))
    captcha=forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

class FormSignUp(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}
    ))
    name=forms.CharField(min_length=1,max_length=12,widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    phone=forms.CharField(min_length=11,max_length=11,error_messages={'min_length':'Length ERROR!','max_length':'Length ERROR!'},
                          widget=forms.TextInput(attrs={'class':'form-control'}
    ))
    work=forms.CharField(min_length=1,max_length=12,widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(min_length=6, max_length=18, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    checkPassword = forms.CharField(min_length=6, max_length=18, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    profile = forms.CharField(min_length=1, max_length=140, widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))
    captcha = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    def clean_checkPassword(self):
        password=self.cleaned_data['password']
        checkPassword=self.cleaned_data['checkPassword']
        if password!=checkPassword:
            raise forms.ValidationError('The two passwords do not match!')
        else:
            return checkPassword

class FormEditUser(forms.Form):
    name=forms.CharField(min_length=1,max_length=12,widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    phone=forms.CharField(min_length=11,max_length=11,error_messages={'min_length':'Length ERROR!','max_length':'Length ERROR!'},
                          widget=forms.TextInput(attrs={'class':'form-control'}
    ))
    work=forms.CharField(min_length=1,max_length=12,widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    profile = forms.CharField(min_length=1, max_length=140, widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))

class FormCreateProject(forms.Form):
    name = forms.CharField(min_length=1, max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    code = forms.CharField(min_length=1, max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    describe=forms.CharField(min_length=1,max_length=140,widget=forms.Textarea(
        attrs={'class':'form-control'}
    ))
    captcha = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    def clean_code(self):
        code=self.cleaned_data['code']
        if code.isalnum():
            return code
        else:
            return ValidationError('code style WRONG!')



class FormEditProject(forms.Form):
    name = forms.CharField(min_length=1, max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    describe=forms.CharField(min_length=0,max_length=140,widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

class FormCreateTask(forms.Form):
    name = forms.CharField(min_length=1, max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    content = forms.CharField(min_length=0, max_length=140, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    '''
    pushTime=forms.DateField(widget=forms.DateInput(
        attrs={'type':'date'}
    ))
    '''
    deadLine = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}
    ))
    member=forms.CharField(max_length=140,widget=forms.Textarea(
        attrs={'class': 'form-control','placeholder':'Members: xxx@xx.xx,xxx@xx.xxx,......'}
    ))

