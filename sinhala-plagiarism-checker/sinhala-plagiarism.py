# -*- coding: utf-8 -*-
import sys
import MySQLdb
import codecs
import re
import string

import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

stopwords = "../StopWords.txt"
stem_dictionary = "../stem_dictionary.txt"

# connect to mysql db
db = MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  		  # your password
                     db="research",       # name of the data base
                     charset='utf8',
                     use_unicode=True)

# # create a Cursor object
cur = db.cursor()

# # select all news articles
sql = "SELECT title, body FROM `newsarticles` WHERE `time` LIKE '2017-02-01%'"# ORDER BY RAND() LIMIT 1000"
cur.execute(sql)

# get all news titles and bodies to one string
text = ""
documents,titles = [],[]
for row in cur.fetchall():
    text = row[0] + " " + row[1]
    documents.append(text)
    titles.append(row[0])


# read all stop words
stopwords = [unicode(l.strip(), 'utf-8') for l in open(stopwords)]


# read stem_dictionary
stem_dict = [unicode(l.strip(), 'utf-8') for l in open(stem_dictionary)]

stem_dictionary = {}
for s in stem_dict:
    s = s.split("\t")
    stem_dictionary[s[0]] = s[1]

def tokenize_and_clean(text):
    tokens = nltk.word_tokenize(text)

    # remove all unnecessary chars
    # get only sinhala unicode charactors
    regex = re.compile(u'[^\u0D80-\u0DFF]', re.UNICODE)
    tokens = [regex.sub('', w) for w in tokens]
    tokens = filter(None, tokens)

    # remove stop words
    tokens = [word for word in tokens if word not in stopwords]

    # find stem using stem_dictionary
    # use same token if not stem found
    for k, v in enumerate(tokens):
        tokens[k] = stem_dictionary.get(v, v)

    return tokens


def combine(arr):
    out = []
    for x in arr:
        out.append(" ".join(x[0]))
    return set(out)


def compute_jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x / float(y)

def generate_ngrams(doc, n):
    temp = tokenize_and_clean(doc)
    temp = ngrams(temp, n)
    temp = Counter(temp).items()
    temp = combine(temp) 
    return temp

def jaccard_similarity(doc1, doc2):
    n = 1
    n1 = generate_ngrams(doc1, n)
    n2 = generate_ngrams(doc2, n)
    j1 = compute_jaccard(n1, n2)

    return j1

    # n = 2
    # n1 = generate_ngrams(doc1, n)
    # n2 = generate_ngrams(doc2, n)
    # j2 = compute_jaccard(n1, n2)

    # return (j1+j2)/2


# open file to save output
f = codecs.open("plagiarism_output.txt","w+", encoding='utf-8')



for i in range(len(documents)-1):
    for j in range(i+1, len(documents)):
        k = jaccard_similarity(documents[i], documents[j])
        print i,j,k
        if k>=0.15 :
            f.write(str(k) + "\n" + titles[i] + "\n" + titles[j] + "\n\n")



# close file
f.close() 

# close db connection
db.close()