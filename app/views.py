import re
import nltk
from django.shortcuts import render 
from app.models import Article

STOPWORDS = set(nltk.corpus.stopwords.words())

def index(request):
    articles = request.user.article_set.all()
    vocab = nltk.probability.FreqDist()
    for article in articles:
        tokens = (token.lower() for token in article.tokens)
        vocab.update(token for token in tokens\
                if token not in STOPWORDS\
                and token.isalpha()\
                and len(token) < 100)
    return render(request, 'app/index.html', {
        'articles': articles,
        'vocab': ((word, freq) for word, freq in vocab.iteritems() if freq >= 100)
    })

