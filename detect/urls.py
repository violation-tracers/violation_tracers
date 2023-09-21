from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'image'

urlpatterns = [
    # 이미지 업로드
    path('upload/', views.upload_image, name='upload_image'),
    # 이미지 목록
    path('list/', views.image_contents_list, name='image_list'),
    # 이미지 디테일
    path('image_detail/<uuid:uuid>/', views.image_detail, name='image_detail'),
    # 이미지 체크
    path('check/<uuid:uuid>/', views.check_image, name='check_image'),
    # 촬영해서 업로드하고 디텍팅
    path('capture/', views.capture, name="capture"),
]