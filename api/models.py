from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Vacancy(models.Model):
    title = models.TextField()
    title_edited = models.TextField(null=True)
    description = models.TextField(null=True)
    description_edited = models.TextField(null=True)


class Cup(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    link = models.TextField(null=True)


class Course(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    link = models.TextField(null=True)


class Confirmation(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=10)


class UserManager(BaseUserManager):
    def create(self, email, password, **validated_data):
        user = self.model(email=self.normalize_email(email), **validated_data)
        user.set_password(password)

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.TextField()
    first_name = models.TextField()
    birth_year = models.IntegerField()
    city = models.TextField()
    university = models.TextField()
    vacancy = models.TextField
    experience = models.TextField()
    email = models.EmailField(unique=True)

    vacancies = models.ManyToManyField(to=Vacancy)
    cups = models.ManyToManyField(to=Cup)
    courses = models.ManyToManyField(to=Course)

    scoring_value = models.FloatField()

    objects = UserManager()

    USERNAME_FIELD = 'email'
