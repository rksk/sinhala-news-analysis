"""
=============================================
Build basic stem-dictionary using shallow learning method
=============================================

Input:
	bag_of_words.txt
		output of make_list_all_tokens.py
  
Output:
	stem_dictionary.txt
		one to one list of tokens and their stems

Remarks:
	this output need to be human verified and edited before using,
	because this shallow learning method will provide an imcompete list
	
Sajith Ekanayaka
01st Oct 2017
"""


# -*- coding: utf-8 -*-
import codecs

# inputs
suffixes = "suffixes_list.txt"
bag_of_words = "bag_of_words.txt"

# outputs
stem_dictionary = "stem_dictionary.txt"
stemmed_bag_of_words = "stemmed_bag_of_words.txt"

# read all bag_of_words
bag_of_words = [unicode(l.strip(), 'utf-8') for l in open(bag_of_words)]
# remove duplicates and sort accesnding order
bag_of_words = sorted(set(bag_of_words))

# read all suffixes list
suffixes = [unicode(l.strip(), 'utf-8') for l in open(suffixes)]
suffixes = filter(None, suffixes)
suffixes.sort(lambda x,y: cmp(len(y), len(x)))

# save sorted suffixes (just to make sure they sorted in correct way)
suffixes_sorted = "suffixes_sorted.txt"
suffixes_sorted = codecs.open(suffixes_sorted,"w+", encoding='utf-8')
for suf in suffixes:
	suffixes_sorted.write(suf + "\n")
suffixes_sorted.close()

# open file to save output
stem_dict = codecs.open(stem_dictionary,"w+", encoding='utf-8')
stemmed_bow = codecs.open(stemmed_bag_of_words,"w+", encoding='utf-8')

prev = ""
stems = {}
found = 0
for w in bag_of_words:
	if prev!="":
		found = 0
		for suf in suffixes:
			if prev + suf == w:
				stems[w] = prev
				stemmed_bow.write(prev + "\n")
				found = 1
				break
	if found == 0 :
		prev = w
		stemmed_bow.write(prev + "\n")

ks = sorted(stems.keys())

for k in ks:
	stem_dict.write(k + "\t" + stems[k] + "\n")


# close file
stem_dict.close()
stemmed_bow.close()
