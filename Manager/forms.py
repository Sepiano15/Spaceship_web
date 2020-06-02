from django import forms #장고에서 지원하는 forms를 import
from .models import myuser
from django.contrib import auth
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=12,widget=forms.PasswordInput,required=True)
    #password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())

    class Meta:
        model = myuser
        fields = ['username', 'password','last_name']

    # def InsertUsername(self,user): #사용자가 중복확인을 완료했을 때 호출된다. form의 아이디에 사용자가 적은 값을 넣는다.
    #     self.Meta.fields[0]=user #중복확인 버튼을 눌러도 입력한 아이디가 사라지지 않는다.

    # def InsertPassword(self,password): 
    #     self.Meta.fields[1]=password

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__( *args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='아이디',widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '아이디를 입력합니다.'}))
    password = forms.CharField(label='비밀번호',widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '비밀번호를 입력합니다.'}))

    class Meta:
        model = myuser
        fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.
        labels = {
            'username' : '아이디',
            'password' : '패스워드'
        }

class UpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['score_one', 'score_two', 'score_three'] 

class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='아이디',widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '아이디를 입력합니다.'}))
    first_name = forms.CharField(label='닉네임',widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '닉네임을 입력합니다.'}))
    password1 = forms.CharField(label='비밀번호',widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '비밀번호를 입력합니다.'}))
    password2 = forms.CharField(label='비밀번호 확인',widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '비밀번호를 입력합니다.'}))

    class Meta:
        model = myuser
        fields = ['username','first_name']
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