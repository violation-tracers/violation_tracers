from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    phone = forms.CharField(
        min_length=12,
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder' : '010-1234-5678'
        })
    )

    name = forms.CharField(
        max_length=20,
        min_length=2,
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'phone', 'email',)