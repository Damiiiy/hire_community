from django.db import models

# Create your models here.


class Users(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)



