from bs4 import BeautifulSoup
import requests
import sys


def scrap(n):

	id = str(n)
	url = "http://www.lankadeepa.lk/columns/%B6%A7/1-" + id
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

	#get date and time
	date = soup.find_all("h4", { "class" : "post-date" })
	if len(date)<1 :
		print "An error occurred!"
		return
	date = date[0].get_text()
	print date.encode('utf8')

	#get article content
	contents = soup.find_all("header", { "class" : "post-content" })
	contents = contents[0].get_text()

	#save content to a file
	file = open("docs/lankadeepa_" + id + ".txt", "w") 
	file.write("<title>" + title.encode('utf8') + "</title>\n") 
	file.write("<time>" + date.encode('utf8') + "</time>\n") 
	file.write("<author></author>\n") 
	file.write("<body>" + contents.encode('utf8') + "</body>") 
	file.close() 
	

# scrap news items by id (from 510500 to 512500)
for n in range(510500, 512500):
	scrap(n)
	print "\n===============================\n\n"
