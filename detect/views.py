from django.shortcuts import render
# 파일 이름 변환을 위한 uuid 모듈
from django.core.files.storage import FileSystemStorage
import uuid
import os
from . import yolov5_detect

# 이미지 파일 업로드 페이지
def index(request):
    return render(request, 'detect/img_up_res.html')

# 이미지 파일 이름 변경 메서드
def rename_imagefile_to_uuid(imagefile_name):
    ext = imagefile_name.split('.')[-1]
    imagefile_name = "%s.%s" % (uuid.uuid4(), ext)
    return imagefile_name

# 이미지 파일에서 객체 인식
def detect(request):
    # 업로드된 image
    detecting_image = request.FILES.get('images')
    fs = FileSystemStorage()

    # 디텍팅할 이미지 파일 이름 변경
    detecting_image_filename = rename_imagefile_to_uuid(detecting_image.name)

    # 디텍팅할 이미지 파일 저장. 저장된 경로 반환
    detecting_image_path = fs.save(detecting_image_filename, detecting_image)

    # 이제 디텍팅할 이미지
    target_image = 'media/' + detecting_image_path

    # 디텍팅할 이미지를 디텍팅 메서드로 보내고,
    # 디텍팅된 이미지의 경로를 반환
    result_img_path = yolov5_detect.y_detect(target_image, detecting_image_path)

    # 디텍팅된 이미지를 보여주는 페이지로 이동
    return render(request, 'detect/result.html', {'image': result_img_path})