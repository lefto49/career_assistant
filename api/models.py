from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField
    first_name = models.CharField
    birth_year = models.IntegerField
    city = models.CharField
    university = models.CharField
    vacancy = models.CharField
    experience = models.CharField
    email = models.EmailField

    USERNAME_FIELD = email