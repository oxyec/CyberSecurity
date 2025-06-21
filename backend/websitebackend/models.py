# models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
# This file defines the Post model for the website backend.
# It includes fields for the title and content of a post.