from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomPasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.update({
            'password_mismatch': '비밀번호가 일치하지 않습니다.',
        })

class CustomUserCreationForm(UserCreationForm):
    # 입력에 유효성 및 예시 작성
    phone = forms.CharField(
        min_length=12,
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder' : '010-1234-5678'
        })
    )
    # 유효성 검사
    name = forms.CharField(
        max_length=20,
        min_length=2,
    )
    # forms 에서 input 창 가져올 경우 사용되는 label 및 input 태그
    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'phone', 'email', "password1", "password2" )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError("이미 사용 중인 사용자명입니다.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("이미 사용 중인 이메일 주소입니다.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('비밀번호가 일치하지 않습니다.')
        return password2
        

