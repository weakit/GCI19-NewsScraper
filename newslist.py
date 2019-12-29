#!/usr/bin/env python3
import json
import time
import tempfile
import webbrowser
import requests as r

API_KEY = 'e80a865f2cf5457eb51771e1b3b26bfa'
ENDPOINT = 'https://newsapi.org/v2/everything?q={}&apiKey={}'
keywords = ('linux', 'open source', 'android')

article_html = open('article.min.html').read()
news_html = open('news.min.html').read()


def get_tags():
    st = keywords[0]
    for keyword in keywords[1:]:
        st += ' • ' + keyword
    return st


def get_list(keyword):
    url = ENDPOINT.format(keyword, API_KEY)
    req = r.get(url)
    if req.status_code == 200:
        return json.loads(req.text)['articles']
    return None


def parse_article(article):
    return {
        'title': article['title'],
        'author': article['author'],
        'description': article['description'],
        'link': article['url'],
        'image': article['urlToImage'],
        'site': article['source']['name']
    }


def render_articles(articles):
    return [article_html.format(**parse_article(article)) for article in articles]


def get_articles():
    articles = []
    for keyword in keywords:
        articles += get_list(keyword)
    return render_articles(articles)


def render_page():
    return news_html.replace('{tags}', get_tags()).replace('{articles}', ''.join(get_articles()))


if __name__ == '__main__':
    print("Scraping news.")
    html = render_page()
    print("Done. Displaying News.")
    temp = tempfile.NamedTemporaryFile(suffix='.html')
    temp.write(html.encode())
    webbrowser.open_new(temp.name)
    time.sleep(5)
    print("Exiting.")

