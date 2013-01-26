from django.db import models

class Article(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=300)
    read = models.BooleanField()
    content = models.TextField()

    def __unicode__(self):
        return '%s' % self.url

