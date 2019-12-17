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
	url = "http://nethnews.lk/article/" + id
	print url

	#get html content from the url
	r  = requests.get(url)
	data = r.text

	# Parse with BeautifulSoup
	soup = BeautifulSoup(data, "lxml")

	#get title
	h1s = soup.find_all("h1", { "class" : "entry-title" })

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
	date = soup.find_all("time", { "class" : "entry-date" })
	if len(date)<1 :
		print "DateTime not found!"
		return
	date = date[0].get_text().encode('utf-8').strip()
	# convert date time to a common format
	# given -> 2017-05-28
	date = datetime.strptime(date, '%Y-%m-%d')
	date = str(date)
	print date

	#get article content
	contents = soup.find_all("div", { "class" : "td-post-content" })
	contents = contents[0].get_text().strip()

	#save content to a file
	file = open("docs/nethnews_" + id + ".txt", "w") #
	file.write("<title>" + title.encode('utf8') + "</title>\n") 
	file.write("<time>" + date.encode('utf8') + "</time>\n") 
	#file.write("<author></author>\n") 
	file.write("<body>" + contents.encode('utf8') + "</body>") 
	file.close() 
	

	sql = "INSERT INTO `newsarticles` (`source`, `sid`, `time`, `title`, `body`) VALUES (%s, %s, %s, %s, %s);"
	
	try:
		cur.execute(sql, ('nethnews', id, date, title, contents))
		db.commit()
	except (MySQLdb.Error, MySQLdb.Warning), e:
		print "SQL Error"
		raise e
	

# scrap news items by id (from 2017/01/01 to present)
for n in range(33500, 42113):
	scrap(n)
	print "\n===============================\n\n"

	
db.commit()
db.close()