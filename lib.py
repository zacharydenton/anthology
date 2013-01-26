import tempfile
import magic
import slate
import requests
from readability import readability
from sklearn.feature_extraction.text import *
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from app.models import Article, PersonalArticle

USER_AGENT = 'Anthology 3.14'

def fetch_article(url):
    try:
        r = requests.get(url, headers={'User-Agent': USER_AGENT})
        if r.status_code != 200: return None
        mimetype = r.headers['content-type']
        if 'application/pdf' in mimetype:
            with tempfile.TemporaryFile() as f:
                for chunk in r.iter_content():
                    f.write(chunk)
                return '\n'.join(slate.PDF(f))
        elif 'text/html' in mimetype:
            return readability.Document(r.text).summary(True)
        elif 'text' in mimetype:
            return r.text
    except Exception as e:
        print e

    return None

def import_pinboard(username, password, user):
    api = requests.get('http://api.pinboard.in/v1/posts/all?format=json', auth=requests.auth.HTTPBasicAuth(username, password))
    for bookmark in api.json():
        try:
            article = Article.objects.get(url=bookmark['href'])
        except Article.DoesNotExist:
            article = Article()
            content = fetch_article(bookmark['href'])
            if not content: continue
            article.url = bookmark['href']
            article.title = bookmark['description']
            article.content = content
            article.save()

        personal, created = PersonalArticle.objects.get_or_create(article=article, user=user)
        if created:
            personal.read = bookmark['toread'] == 'no' 
            personal.liked = True
            personal.save()

def import_reddit(username, password, user):
    def add_link(link, liked):
        try:
            article = Article.objects.get(url=link['url'])
        except Article.DoesNotExist:
            article = Article()
            content = fetch_article(link['url'])
            if not content: return
            article.url = link['url']
            article.title = link['title']
            article.content = content
            article.save()

        personal, created = PersonalArticle.objects.get_or_create(article=article, user=user)
        if created:
            personal.read = True
            personal.liked = liked
            personal.save()

    api = requests.Session()
    api.headers.update({'User-Agent': USER_AGENT})
    api.post('http://www.reddit.com/api/login', {'user': username, 'passwd': password})

    r = api.get('http://www.reddit.com/user/%s/liked.json' % username)
    for link in r.json()['data']['children']:
        add_link(link['data'], True)

    r = api.get('http://www.reddit.com/user/%s/disliked.json' % username)
    for link in r.json()['data']['children']:
        add_link(link['data'], False)

def fetch_reddit():
    api = requests.Session()
    api.headers.update({'User-Agent': USER_AGENT})
    subreddits = ['Foodforthought', 'YouShouldKnow', 'DepthHub', 'TrueReddit']
    for subreddit in subreddits:
        r = api.get('http://www.reddit.com/r/%s/new.json?sort=new' % subreddit)
        for link in r.json()['data']['children']:
            data = link['data']
            try:
                article = Article.objects.get(url=data['url'])
            except Article.DoesNotExist:
                article = Article()
                content = fetch_article(data['url'])
                if not content: continue
                article.url = data['url']
                article.title = data['title']
                article.content = content
                article.save()

def build_classifier(user):
    liked = user.article_set.filter(personalarticle__liked=True)
    disliked = user.article_set.filter(personalarticle__liked=False)
    docs_liked = [article.text for article in liked]
    docs_disliked = [article.text for article in disliked]
    docs = docs_liked + docs_disliked
    labels = [True for doc in docs_liked] + [False for doc in docs_disliked]
    
    classifier = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])
    classifier.fit(docs, labels)

    return classifier
    
def new_articles(user):
    classifier = build_classifier(user)
    docs_new = Article.objects.filter(users__isnull=True)
    predicted = classifier.predict([article.text for article in docs_new])
    return [article for recommended, article in zip(predicted, docs_new) if recommended]


