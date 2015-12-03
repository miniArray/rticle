#! /usr/bin/env python2

# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# the Copyright 2015 simonwjackson <simonwjackson@bowser>
#
# Distributed under terms of the MIT license.

from goose import Goose
import requests
import sys
import cherrypy
import cgi
import signal
import time
import cPickle as pickle

# v0.2
# TODO: D) Filter by URL extension
# TODO: C) Filter out sites like imgur, youtube, etc.

################
# Settings
###############

db_file = "urls.db"
minimum_article_length = 0


################
# functions
###############

def create_db():
    pickle.dump([], open(db_file, "wb" ))
    return []

def load_db():
    return pickle.load(open(db_file, "rb" ))

def get_reddit_json(id):
    headers = {'user-agent': 'my-app/0.0.1'}
    url = "https://www.reddit.com/{id}/top.json?sort=top&t=week".format(id=id)
    r = requests.get(url, headers=headers)
    return r.json()


def get_full_article(url):
    item = ""

    try:
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
    except Exception:
        """ Article failed to parse """
    finally:
        return item


def json_to_feed(list):
    item_entries = ""

    for item in list:
        url = item['data']['url']

        if is_wanted(url, item):
            urls.append(url)
            item_entries += get_full_article(url)

    feed = atom_tmpl.format(title="My Custom Feed", feed_items=item_entries)
    pickle.dump(urls, open(db_file, "wb" ))

    return feed


def is_wanted(url, item):
    is_new = url not in urls
    not_reddit_post = not item['data']['domain'].startswith('self.')
    not_forum_post = "forum" not in url

    return is_new and not_forum_post and not_reddit_post

class App(object):
    @cherrypy.expose
    def reddit(self, id=None):
        json = get_reddit_json(id)
        feed = json_to_feed(json['data']['children'])
        return feed


###############
# Init
###############

with open('atom.tmpl', 'r') as f:
    atom_tmpl = f.read()

with open('item.tmpl', 'r') as f:
    item_tmpl = f.read()

try:
    urls = load_db()
except:
    urls = create_db()

g = Goose()


################
# Main
###############

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 41213,
    })
    cherrypy.quickstart(App())
