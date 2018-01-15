"""
=============================================
Make bag of words from corpus
=============================================

Input:
  mysql table
  
Output:
	bag_of_words.txt
		this will give a unique list of all the sinhala tokens in the given corpus

Sajith Ekanayaka
01st Oct 2017
"""

# -*- coding: utf-8 -*-

import nltk
import sys
import MySQLdb
import codecs
import re

# connect to mysql db
db = MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  		  # your password
                     db="research",       # name of the data base
                     charset='utf8',
                     use_unicode=True)

# create a Cursor object
cur = db.cursor()

# select all news articles
sql = "SELECT title, body FROM `newsarticles`"# LIMIT 10"
cur.execute(sql)

# append all news titles and bodies to one string
text = ""
for row in cur.fetchall():
    text += row[0] + " " + row[1] + " "
	
# tokenize the string
tokens = nltk.word_tokenize(text)

# remove all unnessary chars
# get only sinhala unicode charactors
regex = re.compile(u'[^\u0D80-\u0DFF]', re.UNICODE)
tokens = [regex.sub('', w) for w in tokens]
tokens = filter(None, tokens)

tokens = list(set(tokens)) #this will remove duplicates
tokens = sorted(tokens)

# open file to save output
f = codecs.open("bag_of_words.txt","w+", encoding='utf-8')

# save term frequencies
for c in tokens:
	f.write(c + "\n")

# close file
f.close() 

# close db connection
db.close()