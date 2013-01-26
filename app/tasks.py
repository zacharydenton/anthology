from celery import task
from app.models import Article

@task
def fetch_content():
    lib.fetch_reddit()

@task
def classify_content():
    for article in Article.objects.filter(users__isnull=True):
        for user in User.objects.all():
            lib.classify_article(article, user)
