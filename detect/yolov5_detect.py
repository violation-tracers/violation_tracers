import yolov5
import torch
import os
from PIL import Image
from django.conf import settings

# 이미지에서 객체 인식 메서드
def y_detect(image, image_path):

    # 기본 제공되는 yolov5s 모델 사용
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    # custom 모델 사용
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='model_pt/results64.pt')

    # # 모델 조정 옵션
    model.conf = 0.2 # NMS confidence threshold
    # iou = 0.45  # NMS IoU threshold
    # agnostic = False  # NMS class-agnostic
    # multi_label = False  # NMS multiple labels per box
    # classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
    # max_det = 1000  # maximum number of detections per image
    # amp = False  # Automatic Mixed Precision (AMP) inference

    # 이미지 사이즈를 변경하면서 모델을 이용해 디텍팅
    result = model(image, size=528)

    # 디텍팅된 이미지의 라벨중 마지막 name 만 반환
    # result_detecting_list = result.pandas().xyxy[0]['name'].tolist()
    result_detecting_list = list(map(int, result.pandas().xyxy[0]['name']))
    # print(result_detecting_list)

    # numpy array로 변환
    result.render()

    # media/inferenced_image 폴더에 디텍팅된 이미지 저장
    static_folder = 'media/'
    inferenced_image_path = os.path.join(static_folder, 'inferenced_image')

    # media/inferenced_image 폴더가 없으면 생성
    if not os.path.exists(inferenced_image_path):
        os.makedirs(inferenced_image_path)
    
    # media/inferenced_image/images 폴더가 없으면 생성
    if not os.path.exists(inferenced_image_path + '/images'):
        os.makedirs(inferenced_image_path + '/images')

    # array형태를 이미지로 변환해서 저장
    for img in result.ims:
        img_base64 = Image.fromarray(img)
        # 이미지 저장
        img_base64.save(inferenced_image_path + '/' + image_path)
    
    # 디텍팅된 이미지 경로 반환
    result_url = "inferenced_image/" + image_path
    return (result_url, result_detecting_list)