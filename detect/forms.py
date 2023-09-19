from django import forms
from .models import Image_contents

class ImageContentsForm(forms.ModelForm):
    class Meta:
        model = Image_contents
        exclude = ('check_user', 'check_comment')
        fields = ('image_uuid', 'upload_user', 'uploader_comment')
