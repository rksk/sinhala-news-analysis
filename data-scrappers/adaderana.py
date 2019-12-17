from bs4 import BeautifulSoup
import urllib2
import requests
import sys
import MySQLdb
from datetime import datetime


db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="research",
					 charset='utf8',
                     use_unicode=True)

# create a Cursor object
cur = db.cursor()

# print all the first cell of all the rows
#for row in cur.fetchall():
#    print row[0]


def scrap(n):

	id = str(n)
	url = "http://sinhala.adaderana.lk/"
	print url

	# Fetch URL
	request = urllib2.Request(url)
	request.add_header('Accept-Encoding', 'utf-8')

	# Response has UTF-8 charset header,
	# and HTML body which is UTF-8 encoded
	response = urllib2.urlopen(request, "lxml")
	print response
	return

	# Parse with BeautifulSoup
	soup = BeautifulSoup(response)

	#get title
	h1s = soup.find_all("h2", { "class" : "completeNewsTitle" })

	#if title not found, stop the execution
	if len(h1s)<1 :
		print "An error occurred!"
		return

	title = h1s[0].get_text().strip()
	if len(title)<1 :
		print "An error occurred!"
		return
	print title.encode('utf8')

	#get date and time
	date = soup.find_all("p", { "class" : "newsDateStamp" })
	if len(date)<1 :
		print "An error occurred!"
		return
	date = date[0].get_text().encode('utf-8').strip()
	# convert date time to a common format
	# given -> January 1, 2017&nbsp;&nbsp;10:45 am
	date = date.replace("\xc2\xa0\xc2\xa0", " ")
	date = datetime.strptime(date, '%B %d, %Y %I:%M %p')
	date = str(date)
	print date

	#get article content
	contents = soup.find_all("div", { "class" : "newsContent" })
	contents = contents[0].get_text().strip()

	#save content to a file
	file = open("adaderana_" + id + ".txt", "w") #docs/
	file.write("<title>" + title.encode('utf8') + "</title>\n") 
	file.write("<time>" + date.encode('utf8') + "</time>\n") 
	#file.write("<author></author>\n") 
	file.write("<body>" + contents.encode('utf8') + "</body>") 
	file.close() 
	

	sql = "INSERT INTO `newsarticles` (`source`, `sid`, `time`, `title`, `body`) VALUES (%s, %s, %s, %s, %s);"
	
	try:
		#cur.execute(sql, ('adaderana', id, date, title, contents))
		db.commit()
	except (MySQLdb.Error, MySQLdb.Warning), e:
		print "SQL Error"
		raise e
	

# scrap news items by id (from 2017/01/01 to present)
for n in range(67571, 67572):
	scrap(n)
	print "\n===============================\n\n"

	
db.commit()
db.close()