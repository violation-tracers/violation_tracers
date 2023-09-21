"""
URL configuration for tracers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

def home(request):
    from django.shortcuts import redirect
    # home 화면 변경 시 수정 [임시]
    return redirect('accounts:main')

urlpatterns = [
    # 일단 로그인이 메인화면으로 구성
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('image/',include('detect.urls')),

    path('tracer/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
