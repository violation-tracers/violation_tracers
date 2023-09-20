from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'image'

urlpatterns = [
    # 촬영해놓았던 이미지를 업로드해서 디텍팅
    # path('detect/', views.detect, name="detect"),

    # 이미지 업로드
    path('upload/', views.upload_image, name='upload_image'),
    # 이미지 목록
    path('list/', views.image_contents_list, name='image_list'),
    # 이미지 디테일
    path('image_detail/<uuid:uuid>/', views.image_detail, name='image_detail'),

    # # detecting 후에 result list page를 반환하고, id를 이용해서 해당 image 만 반환
    # path('detail/{int:image_id}/', views.image_detail, name="image_detail"),
    # # 촬영해서 업로드하고 디텍팅
    # path('capture/', views.capture, name="capture"),
]