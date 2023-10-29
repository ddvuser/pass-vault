from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass 

class Folder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=80) 

class Entry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(blank=True)
    note = models.TextField(blank=True, verbose_name="Additional notes")
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True)