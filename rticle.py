from goose import Goose
import requests
import sys
import cherrypy
import cgi
import signal
import time

# v0.1
# TODO: A) A timeout is needed if the parser breaks
# http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call
# http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
# TODO: A) Array of URLS previously parsed

# v0.2
# TODO: D) Filter by URL extension
# TODO: C) Filter out sites like imgur, youtube, etc.

################
# Settings
###############

minimum_article_length = 999

##########################

g = Goose()

def get_reddit_json(id):
    headers = {'user-agent': 'my-app/0.0.1'}
    url = "https://www.reddit.com/{id}/top.json?sort=top&t=week".format(id=id)
    r = requests.get(url, headers=headers)
    return r.json()


def get_full_article(url):
    with open('item.tmpl', 'r') as f:
        item_tmpl = f.read()

    item = ""

    article = g.extract(url=url)
    content = article.cleaned_text

    if content and len(content) >= minimum_article_length:
        title = cgi.escape(article.title.encode('ascii', 'ignore'))

        print(title)
        content = content.encode('ascii','ignore').replace("\n","<br/>\n")
        image = "" #article.top_image.src or ""
        content = cgi.escape(content)

        item = item_tmpl.format(title=title, content=content,
                link=url, date="", image=image)

    return item


def json_to_feed(list):
    with open('atom.tmpl', 'r') as f:
        atom_tmpl = f.read()

    item_entries = ""
    urls = []

    for item in list:
        url = item['data']['url']

        if url not in urls \
                and not item['data']['domain'].startswith('self.') \
                and "forum" not in url:
            urls.append(url)
            item_entries += get_full_article(url)

    feed = atom_tmpl.format(title="My Custom Feed", feed_items=item_entries)
    
    return feed



class App(object):
    @cherrypy.expose
    def reddit(self, id=None):
        json = get_reddit_json(id)
        feed = json_to_feed(json['data']['children'])
        return feed

if __name__ == '__main__':
    cherrypy.quickstart(App())
