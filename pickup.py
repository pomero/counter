#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from itertools import chain
import requests
from urlparse import urlparse
import os
import re

replacePatterns = "<.*?>|\\[\\[.*?\\]\\]|\\[.*?\\]||\\{\\{.*?\\}\\}|\\=\\=.*?\\=\\=|&gt|&lt|&quot|&amp|&nbsp|-|\\||\\!|\\*|'|^[a-zA-Z\\:\\;\\/\\=]$|;|\\(|\\)|\\/|:"

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(root, f)

files = [(f, BeautifulSoup(open(f))) for f in find_all_files("collected")]

def save(f, time, text):
    o = open("pickuped/" + time + os.path.basename(f), "w")
    o.write(text.encode("utf-8"))

for file, soup in files:
    contents = [div for div in soup.find_all("div") if "class" in div.attrs and "single_article_contents" in div["class"] and "editable_contents" in div["class"]]
    words = re.sub(replacePatterns, contents[0].text, "")

    # first date meta = written date time
    timeraw = [header.findChildren("time") for header in soup.find_all("header") if "class" in header.attrs and "single_article_header" in header["class"]]
    datetime = timeraw[0][0]["datetime"]
    save(file, datetime, words)
