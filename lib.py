import requests
from readability.readability import Document
from app.models import Article, PersonalArticle

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
            article.content = content
            article.save()

            personal = PersonalArticle()
            personal.user = user
            personal.article = article
            personal.read = bookmark['toread'] == 'no' 
            personal.liked = True
            personal.save()

def import_reddit(username, password, user):
    def add_link(link, liked):
        try:
            r = requests.get(link['url'])
            if r.status_code != 200: return
            content = Document(r.text).summary(True)
        except:
            return
        if content:
            article = Article()
            article.url = link['url']
            article.title = link['title']
            article.content = content
            article.save()

            personal = PersonalArticle()
            personal.user = user
            personal.article = article
            personal.read = True
            personal.liked = liked
            personal.save()

    api = requests.Session()
    api.headers.update({'User-Agent': 'Anthology 3.14'})
    api.post('http://www.reddit.com/api/login', {'user': username, 'passwd': password})

    r = api.get('http://www.reddit.com/user/%s/liked.json' % username)
    for link in r.json()['data']['children']:
        add_link(link['data'], True)

    r = api.get('http://www.reddit.com/user/%s/disliked.json' % username)
    for link in r.json()['data']['children']:
        add_link(link['data'], False)

