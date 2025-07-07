from django.db import models

class Bulletin(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    link = models.URLField(unique=True)
    published_at = models.DateTimeField()
    image_url = models.URLField(blank=True, null=True)  # Fotoğraf URL alanı
    author = models.CharField(max_length=200, blank=True, null=True)  # Yazar alanı

    def __str__(self):
        return self.title
