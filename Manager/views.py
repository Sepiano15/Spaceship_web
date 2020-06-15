from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login # django.contrib.auth 내 함수 login을 import함.
from django.contrib.auth import logout as auth_logout
from .forms import UserForm, LoginForm, UserChangeForm
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import auth, messages
from django.db.models import Max, Subquery, OuterRef
from .models import myuser

# Create your views here.

#Session Create

def signup(request):
	if request.method == 'POST':
		signup_form = UserCreationForm(request.POST)
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
		original_ranking = user.rank_one
		if original < int(request.POST['score_one']):
			user_score = myuser.objects.all().order_by('-score_one').values() #쿼리셋 내림차순 후 딕셔너리로 변환
			ranking = 1
			for qs in user_score:
				if qs['score_one'] < int(request.POST['score_one']):
					break
				else:
					ranking+=1

			if original_ranking == ranking: #같은 순위일 경우
				user.score_one = request.POST['score_one'] #점수만 갱신
				user.save()
				return redirect('index')
			user.rank_one = ranking #순위 갱신
			user.score_one = request.POST['score_one']
			user.save()
			#기존 사용자들의 순위 조정
			if original_ranking==0: #처음 스코어를 만들었을 때
				original_ranking = len(user_score) #끝까지 수정
			for i in range(ranking-1,original_ranking): #갱신된 순위~원래순위 사이의 값들을 수정
				query = myuser.objects.filter(username=user_score[i]['username'])
				for post in query:
					if post.username == user.username: #자기꺼는 패스
						break
					elif post.rank_one == len(user_score): #꼴찌일땐 패스. 전체 4명인데 5위가 되면 안되서.
						break
					else:
						post.rank_one += 1 #순위 하나씩 늘리고 저장
						post.save()
		return redirect('index')
	return render(request, './update_one.html')


def update_two(request):
	if request.method == 'POST':
		user = request.user
		original = user.score_two
		if original < int(request.POST['score_two']):
			user_score = myuser.objects.all().order_by('-score_two').values()
			i = 1
			for qs in user_score:
				if qs['score_two'] < int(request.POST['score_two']):
					break
				else:
					i+=1
			user.rank_two = i
			user.score_two = request.POST['score_two']
			user.save()
		return redirect('index')
	return render(request, './update_two.html')


def update_three(request):
	if request.method == 'POST':
		user = request.user
		original = user.score_three
		original_ranking = user.rank_three
		if original < int(request.POST['score_three']):
			user_score = myuser.objects.all().order_by('-score_three').values()
			#순위 매기기
			ranking = 1
			for qs in user_score:
				if qs['score_three'] < int(request.POST['score_three']):
					break
				else:
					ranking+=1
			#점수, 순위 갱신
			if original_ranking == ranking: #같은 순위일 경우
				user.score_three = request.POST['score_three'] #점수만 갱신
				user.save()
				return redirect('index')
			user.rank_three = ranking #순위 갱신
			user.score_three = request.POST['score_three']
			user.save()
			#기존 사용자들의 순위 조정
			if original_ranking==0: #처음 스코어를 만들었을 때
				original_ranking = len(user_score) #끝까지 수정
			for i in range(ranking-1,original_ranking): #갱신된 순위~원래순위 사이의 값들을 수정
				query = myuser.objects.filter(username=user_score[i]['username'])
				print(query)
				for post in query:
					if post.username == user.username: #자기꺼는 패스
						break
					elif post.rank_three == len(user_score): #꼴찌일땐 패스. 전체 4명인데 5위가 되면 안되서.
						break
					else:
						post.rank_three += 1 #순위 하나씩 늘리고 저장
						post.save()
				#query.update(rank_three = query['rank_three']+1)

		return redirect('index')
	return render(request, './update_three.html')


def download(request):
	return render(request, './download.html',{})

def glory(request):
	qs1 = myuser.objects.aggregate(score_one=Max('score_one'))
	qs2 = myuser.objects.aggregate(score_two=Max('score_two'))
	qs3 = myuser.objects.aggregate(score_three=Max('score_three'))
	ranker1 = myuser.objects.filter(score_one=qs1['score_one']).values('first_name','score_one')
	ranker2 = myuser.objects.filter(score_two=qs2['score_two']).values('first_name','score_two')
	ranker3 = myuser.objects.filter(score_three=qs3['score_three']).values('first_name','score_three')
	print(ranker3)
	context = {
		'ranker1' : ranker1,
		'ranker2' : ranker2,
		'ranker3' : ranker3,
	}
	return render(request, './glory.html',context)

def blog(request):
	return render(request, './blog.html',{})
