from django.db import models
from django.conf import settings

# Create your models here.
class Image_contents(models.Model):
    # 컨텐츠에 포함된 image의 uuid
    image_uuid = models.CharField(max_length=100)
    # 생성날짜
    create_at = models.DateTimeField(auto_now_add=True)
    # 이미지 업로드 유저 - 유저가 삭제되어도 이미지는 남아있어야 하므로, on_delete=models.SET_NULL
    upload_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='image_contents', null=True)
    # 이미지 확인 유저(관리자) - 관리자가 삭제되어도 지워지면 안 되므로 on_delte = models.set_null null=True
    check_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='check_image_contents', null=True)
    # 이미지 확인 여부(확인 전, 확인 후, 보류)
    check_status = models.IntegerField(default=0)
    # 이미지 업로더의 메모
    uploader_comment = models.TextField(blank=True)
    # 이미지 확인자의 메모
    check_comment = models.TextField(blank=True)
