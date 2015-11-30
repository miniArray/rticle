from goose import Goose
import requests
import sys
import cherrypy
import cgi

# TODO: A timeout is needed if the parser breaks
# http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call
# http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish

# TODO: Minimum article length
# TODO: FIlter by URL extension
# TODO: Filter out sites like imgur, youtube, etc.
# TODO: Array of URLS previously parsed

g = Goose()


with open('atom.tmpl', 'r') as f:
    atom_tmpl = f.read()

with open('item.tmpl', 'r') as f:
    item_tmpl = f.read()


class Index(object):
    @cherrypy.expose
    def reddit(self, id=None):
        headers = {'user-agent': 'my-app/0.0.1'}
        url = "https://www.reddit.com/{id}/top.json?sort=top&t=week".format(id=id)
        r = requests.get(url, headers=headers)
        json = r.json()

        item_entries = ""
        urls = []

        for item in json['data']['children']:
            url = item['data']['url']

            if url not in urls and not item['data']['domain'].startswith('self.'):
                urls.append(url)

                article = g.extract(url=url)
                content = article.cleaned_text

                if content:
                    title = cgi.escape(article.title.encode('ascii', 'ignore'))

                    print(title)
                    content = content.encode('ascii','ignore').replace("\n","<br/>\n")
                    image = "" #article.top_image.src or ""
                    content = cgi.escape(content)

                    item_entries += item_tmpl.format(title=title, content=content,
                            link=url, date="", image=image)

        feed = atom_tmpl.format(title=id, feed_items=item_entries)
        
        return feed


cherrypy.quickstart(Index())



