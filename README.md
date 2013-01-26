Installation
------------

Run the following:

    $ pip install -r requirements.txt
    $ ./manage.py syncdb

Import
------

Next step is to import some data:

    $ ./manage.py shell
    >>> from django.contrib.auth.models import User
    >>> user = User.objects.all()[0]
    >>> import lib
    >>> lib.import_reddit('reddit_username', 'reddit_password', user)
    >>> lib.import_pinboard('pinboard_username', 'pinboard_password', user)

Manipulation
------------

Do some data manipulation:

    $ ./manage.py shell
    >>> from app.models import *
    >>> articles = Article.objects.all()
    >>> article = articles[0]
    >>> print article.url
    http://erlang.org/pipermail/erlang-questions/2013-January/071949.html
    >>> print article.title
    I couldn't really learn Erlang, 'cos it didn't exist, so I invented it.
    >>> print len(article.text)
    9765
    >>> print article.tokens[100:110]
    [u'ok', u'send', u'to', u'machine', u'week', u'3', u'-', u'results', u'The', u'compiler']
    >>> import nltk
    >>> print nltk.sent_tokenize(article.text)[3]
    This is a pretty good environment - teaches you not to make mistakes and to think first.

Server
------

Run the web app:

    $ ./manage.py runserver
    $ curl http://localhost:8000
