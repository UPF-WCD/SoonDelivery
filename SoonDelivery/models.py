from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Test(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class User(AbstractUser):
    school_email = models.TextField(max_length=50, default='')

class Check_list(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.IntegerField()
    place = models.CharField(max_length=30)
    stuffList = models.TextField(default='')

class Stuff(models.Model):
    stuffName = models.CharField(max_length=20)
    check_id = models.ForeignKey(Check_list, on_delete=models.CASCADE)
