from celery import task
import lib
from app.models import Article
from django.contrib.auth.models import User

@task
def fetch_content():
    lib.fetch_reddit()

@task
def classify_content():
    docs_new = Article.objects.filter(users__isnull=True)
    for user in User.objects.all():
        classifier = lib.build_classifier(user)
        predicted = classifier.predict([article.text for article in docs_new])
        print [article for recommended, article in zip(predicted, docs_new) if recommended]
