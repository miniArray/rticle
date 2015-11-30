rticle
======

Convert a subreddit (and others) to a full article [ATOM](https://en.wikipedia.org/wiki/Atom_(standard)) feed. Currently sorted by most popular and limited to the articles of the last 7 days.

Install
-----

Install dependencies:

    pip install goose requests cherrypy

Usage
-----

    python rticle.py

> rticle is currently supported in python 2.7. Try `python2` if the above fails to load

For articles of a subreddit: [http://localhost:8080/reddit?id=r/linux](http://localhost:8080/reddit?id=r/linux)

For articles of a domain: [http://localhost:8080/reddit?id=domain/arstechnica.com](http://localhost:8080/reddit?id=domain/arstechnica.com)

### Todo

* A timeout is needed if the parser breaks
  * http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call
  * http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
* Minimum article length
* FIlter by URL extension
* Filter out sites like imgur, youtube, etc.
* Array of URLS previously parsed
