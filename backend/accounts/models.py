from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, blank=True, null=True)
    github_handle = models.CharField(max_length=50, blank=True, null=True)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

