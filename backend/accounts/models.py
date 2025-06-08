from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, blank=True, null=True)
    github_handle = models.CharField(max_length=50, blank=True, null=True)
