from django import forms #장고에서 지원하는 forms를 import
from .models import myuser
from django.contrib import auth
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class UserForm(forms.ModelForm):
    class Meta:
        model = myuser
        fields = ['first_name', 'score_one', 'score_three']

class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '아이디를 입력합니다.'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '비밀번호를 입력합니다.'}))

    class Meta:
        model = myuser
        fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.
        '''
        labels = {
            'username' : '아이디',
            'password' : '패스워드'
        }
        '''

class UserCreationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '아이디를 입력합니다.'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '닉네임을 입력합니다.'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '비밀번호를 입력합니다.'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '비밀번호를 입력합니다.'}))

    class Meta:
        model = myuser
        fields = ['username','first_name']
        labels = {
            'username' : '아이디',
            'first_name' : '닉네임',
            'password1' : '패스워드',
            'password2' : '패스워드 확인'
        }
        '''
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '아이디를 입력합니다.'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '닉네임을 입력합니다.'}
            ),
            'password1': forms.PasswordInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '비밀번호를 입력합니다.'}
            ),
            'password2': forms.PasswordInput(
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '비밀번호를 다시 한 번 입력합니다.'}
            ),
        }
        '''

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = myuser
        fields = ['username', 'password','last_name']

    def clean_password(self):
        return self.initial["password"]
