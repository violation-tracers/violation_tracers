from django.shortcuts import render
# 파일 이름 변환을 위한 uuid 모듈
from django.core.files.storage import FileSystemStorage
import uuid
import os
from . import yolov5_detect
from .models import ImageContents
import base64
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import redirect
from .forms import ImageContentsForm
from django.shortcuts import get_object_or_404

def detecting(target_image):
    # 이미지파일을 받아왔으니, 이미지경로를 str로 변환
    # 변환된 주소와 이미지를 yolov5_detect.py로 보내서 디텍팅
    # 디텍팅할 이미지
    target_image_path = str(target_image)
    target_image = 'media/' + target_image_path

    # 디텍팅할 이미지를 디텍팅 메서드로 보내고,
    # 디텍팅된 이미지의 경로를 반환
    result_img_path = yolov5_detect.y_detect(target_image, target_image_path)

    # 디텍팅된 이미지를 보여주는 페이지로 이동
    return result_img_path

# image 업로드
# 로그인을 해야 함. 로그인되어있지 않으면 home으로 이동.
# 로그인이 되어있으면 image 업로드 페이지로 이동.
def upload_image(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = ImageContentsForm(request.POST, request.FILES)   
        if form.is_valid():
            image = form.save(commit=False)
            image.upload_user = request.user
            image.save()
            result = detecting(image.image)
            image.detect_result = result[1]
            image.save()
            # to detect image after save

            # return redirect('image_list')
            return render(request, 'image/image_detail.html', {'image_contents': image})
    else:
        form = ImageContentsForm()
    return render(request, 'image/upload_image.html', {'form': form})

# 이미지 리스트
def image_contents_list(request):
    if request.user.is_superuser:
        target_images = ImageContents.objects.all()
    else:
        target_images = ImageContents.objects.filter(upload_user=request.user)
    
    return render(request, 'image/image_list.html', {'image_contents_list': target_images})

# 이미지 상세보기
def image_detail(request, uuid):
    # uuid to string and replace '-' to ''
    uuid = str(uuid).replace('-', '')
    image = get_object_or_404(ImageContents, image_uuid=uuid)
    
    return render(request, 'image/image_detail.html', {'image_contents': image})

# admin은 imagecontents를 확인해서 checking 을 할 수 있어야합니다.
# checking을 하면, check_status가 1로 바뀌고, check_user가 admin으로 바뀌어야 합니다.
# checking을 하면, check_comment를 남길 수 있어야 합니다.
# checking을 하면, check_date가 현재 시간으로 바뀌어야 합니다.
def check_image(request, uuid):
    
    # uuid to string and replace '-' to ''
    target_uuid = str(uuid).replace('-', '')

    if request.user.is_superuser:
        target_image = get_object_or_404(ImageContents, image_uuid=target_uuid)
        # 이미지 체크
        if request.method == 'POST':
            # check_status가 1로 바뀌고, check_user가 admin으로 바뀌어야 합니다.
            target_image.check_status = request.POST['check_status']
            target_image.check_user = request.user
            # check_comment를 남길 수 있어야 합니다.
            if request.POST['check_comment']:
                target_image.check_comment = request.POST['check_comment']
            # check_date가 현재 시간으로 바뀌어야 합니다.
            # image.check_date = timezone.now()
            target_image.save()
            return redirect('image:image_detail', uuid=uuid)
        # 이미지 상세보기
        else:
            return render(request, 'image/check_violation.html', {'image_contents': target_image})
    else:
        # 관리자가 아니라면 home으로 이동
        return redirect('accounts:main')

# 촬영해서 업로드하는 페이지


# video streaming 중 실시간 detecting