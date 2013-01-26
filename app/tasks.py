from celery import task
from app.models import Article

@task
def fetch_content():
    lib.fetch_reddit()

