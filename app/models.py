import nltk
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    users = models.ManyToManyField(User, through='PersonalArticle')

    def __unicode__(self):
        return '%s' % self.url

    @property
    def text(self):
        return nltk.clean_html(self.content)

    @property
    def tokens(self):
        return nltk.word_tokenize(self.text)

class PersonalArticle(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    read = models.BooleanField()
    liked = models.BooleanField()

    def __unicode__(self):
        return '@%s [%s]' % (self.user, self.article.url)

