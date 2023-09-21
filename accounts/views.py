from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from . forms import CustomUserCreationForm

# Create your views here.

# setting.py User 가져오기
User = get_user_model()

# 서버 접속시 바로 들어가는 화면 html
def main(request):

    return render(request, 'accounts/main.html')

# 회원가입 함수
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        # html 에서 POST 형식으로 가져오는 값들 불러오기
        signup_form = CustomUserCreationForm(request.POST)
        # 장고 내에서 유효성 검사 / DB에 저장 / home 화면으로 이동
        if signup_form.is_valid():
            user = signup_form.save()
            group = Group.objects.get(name='reporter')
            user.groups.add(group)
            auth_login(request, user)
            return redirect('home')
    else:
        # Form 객체 생성
        signup_form = CustomUserCreationForm()
    # GET 방식으로 접속시 Input Form을 가지고 HTML로 이동
    return render(request, 'accounts/signup.html', {
        'signup_form' : signup_form,
    })

# 로그인 VIEW
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        # django 내의 구성되어 있는 인증 input form을 가져와서 이동
        login_form = AuthenticationForm()
    else:
        # 인증 input form 에서 가져온 data 들으로 유효성 검사 / 인증 / 정상작동 후 home 이동
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'home')
        
    # GET 방식으로 접속시 form을 가지고 이동
    return render(request, 'accounts/login.html', {
       'login_form' : login_form,
    })
# logout view
def logout(request):
    # django 내에 구현 되어 있는 함수 활용 / session에서의 값을 지운다.
    auth_logout(request)
    return redirect('home')
    