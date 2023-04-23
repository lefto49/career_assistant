from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from api.data.Vacancy import Vacancy

from api.data.Cup import Cup

from api.data.Course import Course

from api.data.UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.TextField()
    first_name = models.TextField()
    birth_year = models.IntegerField()
    city = models.TextField()
    university = models.TextField()
    vacancy = models.TextField()
    experience = models.TextField()
    email = models.EmailField(unique=True)

    vacancies = models.ManyToManyField(to=Vacancy)
    cups = models.ManyToManyField(to=Cup)
    courses = models.ManyToManyField(to=Course)

    scoring_value = models.FloatField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'