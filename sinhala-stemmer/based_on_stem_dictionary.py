"""
=============================================
Sinhala stemming with stem-dictionary
=============================================

Input:
  stem_dictionary.txt
	1.txt, 2.txt, 3.txt, 4.txt, 5.txt

Output:
	based_on_stem_dictionary.txt
		a summary of stemming process will be provided
	1_out_2.txt, 2_out_2.txt, 3_out_2.txt, 4_out_2.txt, 5_out_2.txt
		this contains an one-to-one list of words and their stems for each input document

Remarks:
	The stem dictionary is built using applying the shallow learning method sinhala news corpus,
	and then manually editing the output.

Sajith Ekanayaka
01st Oct 2017
"""

# -*- coding: utf-8 -*-
import codecs
import nltk
import re


report = codecs.open("based_on_stem_dictionary.txt","w+", encoding='utf-8')
total = 0
	
stem_dict = [unicode(l.strip(), 'utf-8') for l in open("stem_dictionary.txt")]
stem_dictionary = {}
for s in stem_dict:
	s = s.split("\t")
	stem_dictionary[s[0]] = s[1]

def run_stemmer(n):
	global total

	doc = str(n) + ".txt"
	stemmed_bag_of_words = str(n) + "_out_2.txt"

	stemmed_bow = codecs.open(stemmed_bag_of_words,"w+", encoding='utf-8')

	doc = [unicode(l.strip(), 'utf-8') for l in open(doc)]
	text = " ".join(doc)

	# tokenize the string
	tokens = nltk.word_tokenize(text)

	# remove all unnessary chars
	# get only sinhala unicode charactors
	regex = re.compile(u'[^\u0D80-\u0DFF]', re.UNICODE)
	tokens = [regex.sub('', w) for w in tokens]
	tokens = filter(None, tokens)

	tokens = list(set(tokens)) #this will remove duplicates
	bag_of_words = sorted(tokens)

	prev = ""
	stems = {}
	found = 0
	for w in bag_of_words:
		v = stem_dictionary.get(w, "")
		if len(v) > 0 :
			stems[w] = v
			stemmed_bow.write(w + ", " + v + "\n")
		else:
			stemmed_bow.write(w + "\n")


	report.write("doc" + str(n) + "\n")
	report.write("Total tokens: " + str(len(tokens)) + "\n")
	report.write("Stemmed tokens : " + str(len(stems)) + "\n")

	pre = 100.0 * len(stems)/len(tokens)
	total = total + pre

	report.write("Stemmed presentage : " + str(pre) + "\n")
	report.write("\n\n")

	# close file
	stemmed_bow.close()



run_stemmer(1)
run_stemmer(2)
run_stemmer(3)
run_stemmer(4)
run_stemmer(5)

report.write("Average : " + str(1.0*total/5) + "\n")
report.close()