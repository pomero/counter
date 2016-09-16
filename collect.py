#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from itertools import chain
import requests
from urlparse import urlparse

# root
ROOT="http://dev.classmethod.jp/author/hakamata/"
f = urllib2.urlopen(ROOT)
soup = BeautifulSoup(f)

# get all pages
aa = [div.findAll("a") for div in soup.find_all("div") if "class" in div.attrs and "pagebar" in div["class"]]
pages = list(set([a["href"] for a in list(chain.from_iterable(aa))]))
pages.append(ROOT)
print(pages)

# get all articles urls
def getArticleUrl(soup):
    titles = [h2.findChild() for h2 in soup.find_all("h2") if "class" in h2.attrs and "title" in h2["class"]]
    return [title["href"] for title in titles]
urls = [getArticleUrl(BeautifulSoup(urllib2.urlopen(page))) for page in pages]
urls = list(chain.from_iterable(urls))
print(urls)

for url in urls:
    print(url)
    text = requests.get(url).text
    f = open(urlparse(url).path.replace("/", "_"), "w")
    f.write(text.encode("utf-8"))
