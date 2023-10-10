# Image_Object_Detection_Project

## Traffic Law Violation Detection

### 서비스 소개
- 개인 이동수단의 증가로 인해 교통 법규 위반 사례의 증가와 사고 사례 또한 증가하게 되고 이를 해결하기 위한 인력은 한정적입니다.
- 한정적인 인력의 효율을 높이기 위해 딥러닝 모델을 이용한 서비스 제공
- 신고자(사용자)가 신고하고자하는 이미지를 저장한 후 Web Service에 접속 후 이미지 업로드를 진행하면 yolov5 모델이 위반사항에 대한 분류를 해주고 관리자(판단하는사람)이 1차 분류에서의 효율성이 개선됨

### 제작기간 & 참여 인원
- 2023.9.5. ~ 2023.10.4.
- 김도현 (Image labeling / Detect Backend / Data Crawling)
- 나상원 (Image labeling / Account / Template Frontend / Web Service Deploy)
- 장주언 (Image labeling / Modeling / Graph Visualization)
### 프로젝트 목적 및 기능
- 딥러닝에 활용되는 모델과 Web Service를 연동 시키고 AWS 에 배포를 통해 Public IP로 접속을 해도 Service 이용을 가능토록 하고자 합니다.
### 주요 기술
- 주요 언어 : Python
- FrameWork : Django
- 딥러닝 모델 : YOLOv5
- 배포 서버 : AWS
- Front End : Bootstrap / CSS / HTML
- DB : Sqlite3
### 구현 기능
- Account 별로 그룹화를 통해 보이는 페이지 구분
- 이미지를 업로드 할 경우 올린 당사자가 올린 이미지만 보는 목록
- 이미지를 YOLOv5 모델을 통해 객체 Detection(Bounding Box)
- 추출된 결과물이 적절하다면 그대로 검출하고 판단하는사람(admin)에 의견을 넣고 싶을 경우 `검토` 버튼을 통해 추가 작업 가능
- 추출된 결과물에 따른 시각화 막대 그래프(통계량) / 일자 별로 filter 기능
- 웹캡으로 연동이 가능하여 웹캠을 통한 이미지 Upload
- 모바일 접속 시 Image Upload Service 실행하면 모바일의 camera 연동 기능
### 추가 및 개선할 사항
- 학습할 이미지의 수가 적었으므로, 모델의 성능 역시 신뢰도가 떨어짐, 이에 따라 더 많은 이미지를 추라적으로 라벨링 / 학습을 시킬 필요가 있음
- 서비스의 성능을 지속적으로 평가하여 모델의 정확도를 개선하고, 객체 검출 오류를 최소화 해야함.
### Review
- 모델의 성능은 개발자가 하이퍼파라미터를 조정하여 향상 시킬 수 있는데, 무조건 많고 높게 조정한다고 좋은 성능이 나오진 않았음.
- 내부평가 지표로 사용하고 있는 P, R, mAP50 등의 수치 역시 무조건 높다고 검출 결과가 좋은것은 아니였음.
- 이미지의 Labeling에 대한 중요성이 크다
- DB 설계에 중요성을 느낌
- 좀 더 나은 서비스가 되기 위해 어떤 데이터가 필요한 지 어떤 데이터를 가져올 수 있는지 고민해볼 수 있는 기회였다.
