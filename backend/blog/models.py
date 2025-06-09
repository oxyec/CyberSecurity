from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)  # Blog başlığı
    content = models.TextField()              # Blog içeriği
    author = models.TextField() # Yazıyı yazan kullanıcı
    created_at = models.DateTimeField(auto_now_add=True)        # Otomatik tarih
    dummy = models.BooleanField(default=False)

    def __str__(self):
        return self.title
