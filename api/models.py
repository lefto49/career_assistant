from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_year = models.IntegerField()
    city = models.CharField(max_length=30)
    university = models.CharField(max_length=100)
    vacancy = models.CharField(max_length=30)
    experience = models.CharField(max_length=1000)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'