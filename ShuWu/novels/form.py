from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off'}),
    )
    password1 = forms.CharField(
        label='密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '6-18位', 'autocomplete': 'off'}),
    )
    password2 = forms.CharField(
        label='确认密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'off'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已存在')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        if len(password1.strip()) > 18 or len(password1.strip()) < 6:
            raise forms.ValidationError('密码长度不符合要求')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', }),
    )

    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', }),
    )

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            password = self.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                self.cleaned_data['user'] = user
                return self.cleaned_data
            else:
                raise forms.ValidationError('密码错误')
        else:
            raise forms.ValidationError('该用户不存在')
