from django.db import models


class Vacancy(models.Model):
    title = models.TextField()
    title_edited = models.TextField(null=True)
    description = models.TextField(null=True)
    description_edited = models.TextField(null=True)