"""
=============================================
Sinhala stemming with shallow learning method
=============================================

Input:
  stem_dictionary.txt
	1.txt, 2.txt, 3.txt, 4.txt, 5.txt

Output:
	realtime_stemming.txt
		a summary of stemming process will be provided
	1_out_1.txt, 2_out_1.txt, 3_out_1.txt, 4_out_1.txt, 5_out_1.txt
		this contains an one-to-one list of words and their stems for each input document

Remarks:
	The concept and the list of suffixes were provided by Mr. Viraj Welgama, UCSC
	The implementation was done to fit my usage.
	Also I ordered the list of suffixes according to descending order their lenghts to improve accuracy.

Sajith Ekanayaka
11th Sept 2017
"""

# -*- coding: utf-8 -*-
import codecs
import nltk
import re

report = codecs.open("realtime_stemming.txt","w+", encoding='utf-8')
total = 0

def run_stemmer(n):
	global total
	suffixes = "suffixes_list.txt"
	doc = str(n) + ".txt"
	stemmed_bag_of_words = str(n) + "_out_1.txt"

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


	# read all suffixes list
	suffixes = [unicode(l.strip(), 'utf-8') for l in open(suffixes)]
	suffixes = filter(None, suffixes)
	suffixes.sort(lambda x,y: cmp(len(y), len(x)))


	prev = ""
	stems = {}
	found = 0
	for w in bag_of_words:
		if prev!="":
			found = 0
			for suf in suffixes:
				if prev + suf == w:
					stems[w] = prev
					stemmed_bow.write(w + ", " + prev + "\n")
					found = 1
					break
		if found == 0 :
			prev = w
			stemmed_bow.write(prev + "\n")


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