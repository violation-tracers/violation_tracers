from datetime import datetime
from django.shortcuts import render
from detect.models import ImageContents
import ast
import platform
from matplotlib import font_manager, rc
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from django.utils.timezone import make_aware


# 한글지원
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':  # 맥OS
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # 윈도우
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system...  sorry~~~')

def create_bar_chart(data_dict, filename, xlabel='', ylabel='', title='', x_names=[]):

    keys = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(12, 6)) 
    plt.bar(keys, values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(keys, x_names)

    # 그래프를 이미지 파일로 저장
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # 이미지를 Base64로 인코딩하여 템플릿으로 전달
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

    plt.close()

    return img_base64

def visualize_data(request):
    # ImageContents 모델에서 모든 데이터 가져오기
    image_contents = ImageContents.objects.all()

    # 데이터를 처리할 빈 딕셔너리 생성
    data_dict1 = {'8': 0, '9': 0, '10': 0, '13': 0}
    data_dict2 = {'5': 0, '6': 0, '12': 0}

    # 데이터를 처리하고 data_dict 업데이트
    for content in image_contents:
        try:
            check_result = ast.literal_eval(content.check_result)
            for key, value in check_result.items():
                if str(key) in data_dict1:
                    data_dict1[str(key)] += value
                elif str(key) in data_dict2:
                    data_dict2[str(key)] += value
        # 아직 검토를 하지 않아 check_result 값이 없을 경우 패스하고 지나감
        except (ValueError, TypeError, SyntaxError):
            pass

    # 그래프 생성 및 이미지로 저장
    img1 = create_bar_chart(data_dict1, 'graph1.png', title='Motorcycle', xlabel='Violation Type', ylabel='Number', x_names=['정지선 위반, 보행자 안전 위협', '불법 주정차, 중앙선 침범','보행자 도로 침범','오토바이 헬맷 미착용'])
    img2 = create_bar_chart(data_dict2, 'graph2.png', title='Car', xlabel='Violation Type', ylabel='Number', x_names=['정지선 위반, 보행자 안전 위협', '불법 주정차, 중앙선 침범', '보행자 도로 침범'])

    return render(request, 'visualization/bar_visualization.html', {'img1': img1, 'img2': img2})

def visualize_data_by_date(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        start_date = make_aware(start_date)  # 타임존 정보를 추가하여 비교
        end_date = make_aware(end_date)  # 타임존 정보를 추가하여 비교

        # 시작 날짜와 종료 날짜 사이의 DB 데이터 필터링
        image_contents = ImageContents.objects.filter(create_at__date__range=[start_date.date(), end_date.date()])

        # 데이터를 처리할 빈 딕셔너리 생성
        data_dict1 = {'8': 0, '9': 0, '10': 0, '13': 0}
        data_dict2 = {'5': 0, '6': 0, '12': 0}

        # 데이터를 처리하고 data_dict 업데이트
        for content in image_contents:
            check_result = ast.literal_eval(content.check_result)
            for key, value in check_result.items():
                if str(key) in data_dict1:
                    data_dict1[str(key)] += value
                elif str(key) in data_dict2:
                    data_dict2[str(key)] += value

        # 그래프 생성 및 이미지로 저장
        img1 = create_bar_chart(data_dict1, 'graph1.png', title='Motorcycle', xlabel='Violation Type', ylabel='Number', x_names=['정지선 위반, 보행자 안전 위협', '불법 주정차, 중앙선 침범','보행자 도로 침범','오토바이 헬맷 미착용'])
        img2 = create_bar_chart(data_dict2, 'graph2.png', title= 'car', xlabel='Violation Type', ylabel='Number', x_names=['정지선 위반, 보행자 안전 위협', '불법 주정차, 중앙선 침범', '보행자 도로 침범'])

        return render(request, 'visualization/bar_visualization.html', {'img1': img1, 'img2': img2})

    return render(request, 'visualization/select_date.html')