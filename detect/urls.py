from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # 이미지를 어떻게 업로드할지 선택하는 페이지
    path('', views.index, name="index"),
    # 촬영해놓았던 이미지를 업로드해서 디텍팅
    path('detect/', views.detect, name="detect"),
    # image list page를 반환
    path('list/', views.image_list, name="image_list"),
    # detecting 후에 result list page를 반환하고, id를 이용해서 해당 image 만 반환
    path('/detail/{int:image_id}/', views.image_detail, name="image_detail"),
    # # 촬영해서 업로드하고 디텍팅
    # path('capture/', views.capture, name="capture"),
]