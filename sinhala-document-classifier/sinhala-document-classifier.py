# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import linear_model

# from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score

import codecs
import nltk
import re

import MySQLdb
stopwords = "StopWords.txt"
stem_dictionary = "stem_dictionary.txt"
clustering_output = "clustering_output.txt"

db = MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  		  # your password
                     db="research",       # name of the data base
					 charset='utf8',
                     use_unicode=True)


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


def run_classifier():

    global db, stopwords

    # create a Cursor object
    cur = db.cursor()

    sql = "SELECT cat, count(id) FROM `newsarticles` WHERE cat<>'' GROUP BY cat"
    cur.execute(sql)

    train_docs = {}
    test_docs = []
    for row in cur.fetchall():
        train_docs[row[0]] = ""

    sql = "SELECT title, body, cat, id FROM `newsarticles` WHERE cat<>'' ORDER BY RAND()"
    cur.execute(sql)

    train_doc_percentage = 0.7
    count = 0
    rows = cur.fetchall()
    train_limit = train_doc_percentage * len(rows)
    for row in rows:
        text = row[0] + " " + row[1]
        if(count <= train_limit):
            train_docs[row[2]] += text + " "
        else:
            test_docs.append([text, row[2]])
        count+=1

    train_data = []
    y_train = []
    for k in train_docs.keys():
        train_data.append(train_docs[k])
        y_train.append(k)


    #instantiate classifier and vectorizer
    # classifier = MultinomialNB()
    classifier = MultinomialNB(alpha=0.1)
    # classifier = GaussianNB() #  A sparse matrix was passed, but dense data is required
    # classifier = BernoulliNB()
    # classifier = BernoulliNB(binarize=0.0)
    # classifier = linear_model.SGDClassifier()

    # vectorize the text (convert the strings to numeric features)
    # vectorizer = TfidfVectorizer()
    # vectorizer = TfidfVectorizer(stop_words=stopwords)
    # vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean)
    vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean, stop_words=stopwords)
    # vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean, ngram_range=(1,2), stop_words=stopwords)
    # vectorizer = CountVectorizer()
    # vectorizer = CountVectorizer(tokenizer=tokenize_and_clean, ngram_range=(1, 2))

    #Apply vectorizer to training data
    X_train=vectorizer.fit_transform(train_data)

    #Train classifier
    classifier.fit(X_train, y_train)

    y_test = []
    predicted = []
    for doc in test_docs:
        cat = classifier.predict(vectorizer.transform([doc[0]]))
        y_test.append(doc[1])
        predicted.append(cat)

    return accuracy_score(y_test, predicted)



experiment_name = "01"

total = 0
count = 0
output = codecs.open(experiment_name + ".txt","w+", encoding='utf-8')
for i in range(100):
    k = run_classifier()
    output.write(str(k) + "\n")	
    total += k
    count += 1

avg = total/count
output.write("\n\nAverage\n")
output.write(str(avg) + "\n")	
output.close()


db.close()