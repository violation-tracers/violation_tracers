from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 임시 메인
    # /main/
    path('', views.main, name='main'),
    # /account/singup/
    path('signup/', views.signup, name='signup'),
    # /accounts/login/
    path('login/', views.login, name='login'),
    # /accounts/logout/
    path('logout/', views.logout, name='logout'),
]
