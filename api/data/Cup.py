from django.db import models


class Cup(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    link = models.TextField(null=True)