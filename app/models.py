from django.db import models

class Article(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=300)
    read = models.BooleanField()
    content = models.TextField()

