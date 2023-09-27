from django.shortcuts import render
# 파일 이름 변환을 위한 uuid 모듈
from django.core.files.storage import FileSystemStorage
import uuid
import os
from . import yolov5_detect
from .models import ImageContents
import base64
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
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
    
    # if request.user.is_superuser:
    if not request.user.groups.filter(name='reporter').exists():
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

    image_list_length = ImageContents.objects.all().count()
    current_index = image.id

    pre_image = None
    next_image = None

    if current_index > 1:
        pre_image = ImageContents.objects.filter(id__lt=image.id).order_by('-id').first()
    if current_index < image_list_length:
        next_image = ImageContents.objects.filter(id__gt=image.id).order_by('id').first()

    violation_status = model_output.chaser(image.detect_result)
    if image.check_result:
        check_result = eval(image.check_result)
        if type(check_result) == tuple:
            check_result = check_result[0]
        check_result_list = []
        for status, num in check_result.items():
            if num:
                if status == 8:
                    sentence = '오토바이 정지선 위반 혹은 보행자 안전 위협 ' + str(num) +  '대'
                    check_result_list.append(sentence)
                elif status == 9:
                    sentence = '오토바이 불법 주정차 혹은 중앙선 침범 ' + str(num) + ' 대'
                    check_result_list.append(sentence)
                elif status == 10:
                    sentence = '오토바이 보행자 도로 침범 ' + str(num) + ' 대'
                    check_result_list.append(sentence)
                elif status == 13:
                    sentence = '오토바이 헬맷 미착용 ' + str(num) + ' 대'
                    check_result_list.append(sentence)
                elif status == 5:
                    sentence = '자동차 정지선 위반 혹은 보행자 안전 위협 ' + str(num) + ' 대'
                    check_result_list.append(sentence)
                elif status == 6:
                    sentence = '자동차 불법 주정차 혹은 중앙선 침범 ' + str(num) + ' 대'
                    check_result_list.append(sentence)
                elif status == 12:
                    sentence = '자동차 보행자 도로 침범 ' + str(num) + ' 대'
                    check_result_list.append(sentence)

        return render(request, 'image/image_detail.html', {
            'image_contents': image,
            'pre_image_uuid': pre_image.image_uuid if pre_image else None,
            'next_image_uuid': next_image.image_uuid if next_image else None,
            'violation_status': violation_status,
            'check_violation_status': check_result_list,
        })
    return render(request, 'image/image_detail.html', {
        'image_contents': image,
        'pre_image_uuid': pre_image.image_uuid if pre_image else None,
        'next_image_uuid': next_image.image_uuid if next_image else None,
        'violation_status': violation_status,
    })

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

# 자동으로 디텍팅한 결과를 뽑아주는 메서드
def auto_checking(detect_result, collect_detect):
    if collect_detect:
        detect_result_list = eval(detect_result)
    else:
        detect_result_list = detect_result
    check_result = {
        8:0,    # 오토바이 흰색선, 정지선 위반 혹은 보행자 안전 위협
        9:0,    # 오토바이 황색선, 불법 주정차 혹은 중앙선 침범
        10:0,   # 오토바이 보행자 도로 침범
        13:0,    # 오토바이 헬맷 미착용
        5:0,    # 자동차 흰색선, 정지선 위반 혹은 보행자 안전 위협
        6:0,    # 자동차 황색선, 불법 주정차 혹은 중앙선 침범
        12:0,    # 자동차 보행자 도로 침범
    }

    for detect_result in set(detect_result_list):
        if int(detect_result) in check_result.keys():
            if collect_detect:
                check_result[detect_result] = detect_result_list.count(detect_result)
            else:
                check_result[int(detect_result)] = detect_result_list[detect_result]

    if collect_detect:
        # 오토바이 수
        motorbike_num = detect_result_list.count(8) + detect_result_list.count(9) + detect_result_list.count(10) + detect_result_list.count(7)
        # 헬멧 수
        helmet_num = detect_result_list.count(11)
    else:
        motorbike_num = 0
        helmet_num = 0
        if "8" in detect_result_list.keys():
            motorbike_num += detect_result_list["8"]
        if "9" in detect_result_list.keys():
            motorbike_num += detect_result_list["9"]
        if "10" in detect_result_list.keys():
            motorbike_num += detect_result_list["10"]
        if "7" in detect_result_list.keys():
            motorbike_num += detect_result_list["7"]
        
        if "11" in detect_result_list.keys():
            helmet_num += detect_result_list["11"]

    if motorbike_num > helmet_num:
        check_result[13] = motorbike_num - helmet_num
    return check_result

# 이미지 확인. 통과. pass
def collect_image(request, uuid):
    target_uuid = str(uuid).replace('-', '')
    # 관리자 여부 확인
    if not request.user.groups.filter(name='reporter').exists():
        
        target_image = get_object_or_404(ImageContents, image_uuid=target_uuid)
        
        # 이미 확인된 이미지가 아니라면, 확인 상태를 1로 바꾸고, 자동으로 디텍팅한 결과를 뽑아주는 메서드
        
        # check_status가 1(예측 결과 적합으로 자동 확인)
        target_image.check_status = 1
        target_image.check_user = request.user
        target_image.check_result = auto_checking(target_image.detect_result, True)
        target_image.check_comment = '통과'
        target_image.check_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        target_image.save()
        return redirect('image:image_detail', uuid=uuid)
        # return HttpResponse(status=200)
    else:
        return redirect('accounts:main')
        # return HttpResponse(status=403)


# 이미지 확인 기능. 관리자만 가능
def check_image(request, uuid):
    
    # uuid to string and replace '-' to ''
    target_uuid = str(uuid).replace('-', '')

    # superuser인지 확인
    # if request.user.is_superuser:
    if not request.user.groups.filter(name='reporter').exists():
        target_image = get_object_or_404(ImageContents, image_uuid=target_uuid)
        # 이미지 체크
        if request.method == 'POST' and request.body:

            data = json.loads(request.body.decode('utf-8'))
            check_comment = data.pop('check_comment')

            # check_status가 2(예측 결과 부적합으로 관리자가 결과 확인)
            target_image.check_status = 2
            target_image.check_user = request.user
            target_image.check_result = auto_checking(data, False)
            if check_comment:
                target_image.check_comment = check_comment
            else:
                target_image.check_comment = target_image.check_comment
            # check_date가 현재 시간으로 바뀌어야 합니다.
            # asio/seoul 기준의 시간대로 timezone 설정
            target_image.check_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            target_image.save()
            return redirect('image:image_detail', uuid=uuid)
        # 이미지 상세보기
        else:
            return render(request, 'image/check_violation.html', {'image_contents': target_image})
    else:
        # 관리자가 아니라면 home으로 이동
        return redirect('accounts:main')

# video streaming 중 실시간 detecting