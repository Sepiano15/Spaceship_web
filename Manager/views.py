from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login # django.contrib.auth 내 함수 login을 import함.
from django.contrib.auth import logout as auth_logout
from .forms import UserForm, LoginForm, UserChangeForm, UpdateForm
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import auth, messages

# Create your views here.

#Session Create
def signup(request):
	if request.method == 'POST':
		signup_form = UserCreationForm(request.POST)
		print(signup_form)
		if signup_form.is_valid():
			signup_form.save()
			return redirect('index')
	else:
		signup_form = UserCreationForm()

	return render(request, './signup.html',{'signup_form':signup_form})

def index(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request,'사용자 이름과 비밀번호가 일치하지 않습니다.')
            return redirect('index')
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form})

#DB에서 TOP 10의 닉네임과 점수를 가져와서 디렉토리로 만든다.
#form으로 만들어서 템플릿에 전송하면 그 내용을 출력한다.

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        return redirect('index')
    
    else:
        login_form = LoginForm()
    
    return render(request, './index.html', {'login_form' : login_form})

def logout(request):
    auth_logout(request)
    return redirect('index')
'''
def update(request):
	if request.method == 'POST':
		update_form = UpdateForm(request.POST, instance=request.user)
		if update_form.is_valid():
			update_form.save()
			return redirect('index')

	else:
		update_form = UpdateForm(instance=request.user)
		return render(request, './update.html', {'update_form' : update_form})
'''
def update_one(request):
	if request.method == 'POST':
		user = request.user
		original = user.score_one
		if original < int(request.POST['score_one']):
			user.score_one = request.POST['score_one']
			user.save()
		return redirect('index')
	return render(request, './update_one.html')


def update_two(request):
	if request.method == 'POST':
		user = request.user
		original = user.score_two
		if original < int(request.POST['score_two']):
			user.score_two = request.POST['score_two']
			user.save()
		return redirect('index')
	return render(request, './update_two.html')


def update_three(request):
	if request.method == 'POST':
		user = request.user
		original = user.score_three
		if original < int(request.POST['score_three']):
			user.score_three = request.POST['score_three']
			user.save()
		return redirect('index')
	return render(request, './update_three.html')


def download(request):
	return render(request, './download.html',{})

def glory(request):
	return render(request, './glory.html',{})

def blog(request):
	return render(request, './blog.html',{})
