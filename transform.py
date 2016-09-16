#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import MeCab
import os

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(root, f)

files = [f for f in find_all_files("pickuped")]

mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

for f in files:
    text = open(f).read()
    transformed = mecab.parse(text)
    out = open("transformed/" + os.path.basename(f), "w")
    out.write(transformed)
