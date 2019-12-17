# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys


def scrap(n):

	id = str(n)
	url = "http://www.silumina.lk/node/" + id
	print url

	#get html content from the url
	r  = requests.get(url)
	data = r.text

	#parse with BS
	soup = BeautifulSoup(data, "lxml")

	#get title
	h1s = soup.find_all('h1')

	#if title not found, stop the execution
	if len(h1s)<1 :
		print "An error occurred!"
		return

	title = h1s[0].get_text()
	print title.encode('utf8')
		
	#get category
	category = soup.find_all("div", { "class" : "field-name-field-section" })
	if len(category)>0 :
		category = category[0].get_text()
		print category.encode('utf8')
	else:
		category = ""
		
	#filter a few categories only
	if category!=u"පුවත්" and category!=u"දේශපාලනය" and category!=u"ක්‍රීඩා" and category!=u"විශේෂාංග" and category!=u"විදෙස්" :
		print "skipping category " + category
		return
		

	#get date
	date = soup.find_all("span", { "class" : "date-display-single" })
	if len(date)<1 :
		print "An error occurred!"
		return
	date = date[0].get_text()
	print date.encode('utf8')

	#get author
	author = soup.find_all("div", { "class" : "field-name-field-author" })
	if len(author)>0 :
		author = author[0].get_text()
		print author.encode('utf8')
	else:
		author = ""

	#get article content
	contents = soup.find_all("div", { "class" : "field-name-body" })
	if len(contents)<1 :
		print "An error occurred!"
		return
	contents = contents[0].get_text()

	#save content to a file
	file = open("docs/silumina_" + id + ".txt", "w") #
	file.write("<title>" + title.encode('utf8') + "</title>\n") 
	file.write("<time>" + date.encode('utf8') + "</time>\n") 
	file.write("<author>" + author.encode('utf8') + "</author>\n") 
	file.write("<body>" + contents.encode('utf8') + "</body>") 
	file.close() 
	

# scrap news items by id (from 1 to 3470)
for n in range(1, 3470):
	scrap(n)
	print "\n===============================\n\n"
