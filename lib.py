import requests
from readability.readability import Document
from app.models import Article

def import_pinboard(username, password, user):
    api = requests.get('http://api.pinboard.in/v1/posts/all?format=json', auth=requests.auth.HTTPBasicAuth(username, password))
    for bookmark in api.json():
        try:
            r = requests.get(bookmark['href'])
            if r.status_code != 200: continue
            content = Document(r.text).summary(True)
        except:
            continue
        if content:
            article = Article()
            article.url = bookmark['href']
            article.title = bookmark['description']
            article.read = bookmark['toread'] == 'no'
            article.content = content
            article.save()
            article.users.add(user)

