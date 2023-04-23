from django.db import models


class Course(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    link = models.TextField(null=True)