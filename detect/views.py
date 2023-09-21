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
from . import model_output
import datetime

# 이미지 디텍팅 메서드
# 이미지파일을 받아왔으니, 이미지경로를 str로 변환
# 변환된 주소와 이미지를 yolov5_detect.py로 보내서 디텍팅
def detecting(target_image):

    # 디텍팅할 이미지
    target_image_path = str(target_image)
    target_image = 'media/' + target_image_path

    # 디텍팅할 이미지를 yolov5_detect.py의 디텍팅 메서드로 보내고,
    # 디텍팅된 이미지의 경로와 디텍팅된 클래스 리스트를 반환
    result_url, result_detecting_list = yolov5_detect.y_detect(target_image, target_image_path)
    return (result_url, result_detecting_list)

# image 업로드
# 로그인을 해야 함. 로그인되어있지 않으면 home으로 이동.
# 로그인이 되어있으면 image 업로드 페이지로 이동.
def upload_image(request):
    # 로그인 확인
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # 이미지 업로드
    if request.method == 'POST':
        form = ImageContentsForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.upload_user = request.user
            image.save()
            # (디텍팅된 이미지의 경로, 디텍팅된 클래스 리스트)를 반환
            result = detecting(image.image)
            # 디텍팅 리스트를 이미지 클래스에 저장
            image.detect_result = result[1]
            image.save()

            # 이미지와 함께 이미지 상세보기 페이지로 이동
            return redirect('image:image_detail', uuid=image.image_uuid)
    
    # 이미지 업로드 페이지
    else:
        form = ImageContentsForm()
    return render(request, 'image/upload_image.html', {'form': form})

# 이미지 리스트
def image_contents_list(request):
    # 관리자는 모든 이미지를 볼 수 있음

    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.user.is_superuser:
        target_images = ImageContents.objects.all()
    
    # 일반 유저는 자신의 이미지만 볼 수 있음
    else:
        target_images = ImageContents.objects.filter(upload_user=request.user)
    
    return render(request, 'image/image_list.html', {'image_contents_list': target_images})

# 이미지 상세보기
def image_detail(request, uuid):
    # uuid to string and replace '-' to ''
    uuid = str(uuid).replace('-', '')
    image = get_object_or_404(ImageContents, image_uuid=uuid)
    violation_status = model_output.chaser(image.detect_result)
    return render(request, 'image/image_detail.html', {
        'image_contents': image,
        'violation_status': violation_status
    })

# 이미지 확인 기능. 관리자만 가능
def check_image(request, uuid):
    
    # uuid to string and replace '-' to ''
    target_uuid = str(uuid).replace('-', '')

    # superuser인지 확인
    if request.user.is_superuser:
        target_image = get_object_or_404(ImageContents, image_uuid=target_uuid)
        # 이미지 체크
        if request.method == 'POST':
            # check_status가 1로 바뀌고, check_user가 admin으로 바뀌어야 합니다.
            target_image.check_status = request.POST['check_status']
            target_image.check_user = request.user
            # check_comment를 남길 수 있어야 합니다.(선택)
            if request.POST['check_comment']:
                target_image.check_comment = request.POST['check_comment']
            # check_date가 현재 시간으로 바뀌어야 합니다.
            target_image.check_date = datetime.datetime.now()
            target_image.save()
            return redirect('image:image_detail', uuid=uuid)
        # 이미지 상세보기
        else:
            return render(request, 'image/check_violation.html', {'image_contents': target_image})
    else:
        # 관리자가 아니라면 home으로 이동
        return redirect('accounts:main')

# 촬영해서 업로드하는 페이지
def capture(request):

    # 로그인 필요
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        data = json.loads(request.body)

        # client json으로 보내주는 이름에 맞춰서 받아옴
        image_data = data.get('image')

        if image_data:
            image_data = image_data.replace('data:image/png;base64,', '')
            image_data = base64.b64decode(image_data)

            # image name은 저장되는 날짜를 이름으로 함
            image_name = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.jpg'
            
            with open(f'media/images/{image_name}', 'wb') as f:
                f.write(image_data)

            image = ImageContents()
            # image = image.save(commit=False)
            image.image = f'images/{image_name}'
            image.upload_user = request.user
            image.save()
            result = detecting(image.image)
            image.detect_result = result[1]
            image.save()

            return JsonResponse({"image":image.image_uuid})
    else:
        form = ImageContentsForm()
    return render(request, 'image/capture.html', {'form': form})

# video streaming 중 실시간 detecting