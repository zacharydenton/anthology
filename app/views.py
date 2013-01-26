import re
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.models import Article

@login_required
def index(request):
    articles = request.user.article_set.filter(personalarticle__read=False)
    return render(request, 'app/index.html', locals())
