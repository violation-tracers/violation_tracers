import yolov5
import torch
import os
from PIL import Image
from django.conf import settings

# 이미지에서 객체 인식 메서드
def y_detect(image, image_path):

    # 어떤모델을 쓸 것인지.
    # 기본 제공되는 yolov5s 모델 사용
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    # custom 모델 사용
    # model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

    # 이미지 사이즈를 변경하면서 모델을 이용해 디텍팅
    result = model(image, size=416)

    # numpy array로 변환
    result.render()

    # media/inferenced_image 폴더에 디텍팅된 이미지 저장
    static_folder = 'media/'
    inferenced_image_path = os.path.join(static_folder, 'inferenced_image')

    # media/inferenced_image 폴더가 없으면 생성
    if not os.path.exists(inferenced_image_path):
        os.makedirs(inferenced_image_path)
    
    # array형태를 이미지로 변환해서 저장
    for img in result.ims:
        img_base64 = Image.fromarray(img)
        img_base64.save(f"{inferenced_image_path}/{image_path}")
    
    # 디텍팅된 이미지 경로 반환
    result_url = "inferenced_image/" + image_path
    return result_url