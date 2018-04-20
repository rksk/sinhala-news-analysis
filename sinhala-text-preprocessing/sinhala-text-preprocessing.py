# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import linear_model

import codecs
import nltk
import re

stopwords = "../StopWords.txt"
stem_dictionary = "../stem_dictionary.txt"

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




x_train,y_train,x_test,y_test,all_docs,count = [],[],[],[],[],{}

train_doc_percentage = 0.7
rows = 100
train_limit = train_doc_percentage * rows

for cat in cats:
    count[cat] = 0
    dir = "docs/docs2/" + cat
    for file in os.listdir(dir):
        if file.endswith(".txt"):
            with open(os.path.join(dir, file), 'r') as myfile:
                all_docs.append([cat, myfile.read().replace('\n', '')])


random.shuffle(all_docs)
for doc in all_docs:
    if(count[doc[0]] <= train_limit):
        x_train.append(doc[1])
        y_train.append(doc[0])
    else:
        x_test.append(doc[1])
        y_test.append(doc[0])
    count[doc[0]] = count[doc[0]] + 1

# print count
# print len(x_train),len(y_train),len(x_test),len(y_test)
# exit()

#instantiate classifier and vectorizer
classifier = MultinomialNB(alpha=0.1)

# vectorize the text (convert the strings to numeric features)
vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean, stop_words=stopwords)#, max_df=0.4)
# vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean, stop_words=stopwords, ngram_range=(1,2))
# vectorizer = TfidfVectorizer(tokenizer=tokenize_and_clean, stop_words=stopwords, ngram_range=(2,2))

#Apply vectorizer to training data
X_train=vectorizer.fit_transform(x_train)

#Train classifier
classifier.fit(X_train, y_train)

with open('classification_model.pkl', 'wb') as fout:
    pickle.dump((vectorizer, classifier), fout)



print("--- %s seconds ---" % (time.time() - start_time))