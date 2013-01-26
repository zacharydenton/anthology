import re
import nltk
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.models import Article

STOPWORDS = set(nltk.corpus.stopwords.words())

@login_required
def index(request):
    articles = request.user.article_set.filter(personalarticle__read=False)
    return render(request, 'app/index.html', locals())
