# -*- coding: utf-8 -*-
import time
start_time = time.time()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.pipeline import make_pipeline

import numpy as np

import codecs
import nltk
import re
import sys

import MySQLdb
stopwords = "../StopWords.txt"
stem_dictionary = "../stem_dictionary.txt"

db = MySQLdb.connect(host="127.0.0.1",    # host
                     user="root",         # username
                     passwd="",  		  # password
                     db="research",       # database name
					 charset='utf8',
                     use_unicode=True)

# create a Cursor object
cur = db.cursor()


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

	# find stem using stem_dictionary
	# use same token if not stem found
	for k, v in enumerate(tokens):
		tokens[k] = stem_dictionary.get(v, v)

	return tokens



def run_clustering(number_of_clusters):

	month = 8
	cat = "world" 

	clustering_output = "clustering_0%d_%s.txt" % (number_of_clusters,cat)
	sql = "SELECT title, body, id FROM `newsarticles` WHERE time >= '2017-0%d-01' AND cat2='%s' LIMIT 150" % (month, cat)
	cur.execute(sql)

	documents,titles = [],[]
	for row in cur.fetchall():
		text = row[0] + " " + row[1]
		#text = text.translate(None, string.punctuation)
		documents.append(text)
		titles.append(row[0])


	print "total documents: %d" % len(documents)

	hasher = TfidfVectorizer(tokenizer=tokenize_and_clean, stop_words=stopwords)#, max_df=0.7)
	vectorizer = make_pipeline(hasher, TfidfTransformer())
	# documents is a list of all text in a given article
	X_train_tfidf = vectorizer.fit_transform(documents)

	km = KMeans(init='k-means++', max_iter=100000, n_init=1, n_clusters=number_of_clusters)
	# km.fit(X_train_tfidf)
	clusters = km.fit_predict(X_train_tfidf)


	clusters_out,tags_out,titles_out = [],[],[]

	output = codecs.open(clustering_output,"w+", encoding='utf-8')

	order_centroids = km.cluster_centers_.argsort()[:, ::-1]
	terms = hasher.get_feature_names()
	for i in range(number_of_clusters):
		output.write("cluster %d\n\n" % (i+1))
		for ind in order_centroids[i, :15]:
			tags_out.append(terms[ind])
		output.write(", ".join(tags_out) + "\n\n")

		members = np.where(clusters==i)[0]
		for i in members:
			# titles_out.append(titles[i])
			output.write(titles[i] + "\n")

		output.write("\n\n\n")
		# clusters_out.append({'tags': tags_out, 'titles': titles_out})
		tags_out,titles_out = [],[]



	output.close()


for n in range(3, 11):
	run_clustering(n)


print("--- %s seconds ---" % (time.time() - start_time))

db.close()