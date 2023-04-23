from django.db import models


class Confirmation(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=10)