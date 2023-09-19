from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

def validate_phone(phone):
    if phone[:4] != '010-':
        raise ValidationError(" '010-' 로 시작해주세요.")

class User(AbstractUser):

    # User name
    name = models.CharField(max_length=10)
    # User phone
    phone = models.CharField(max_length=20, validators=[validate_phone])
