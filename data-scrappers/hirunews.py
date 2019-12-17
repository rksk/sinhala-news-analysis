from bs4 import BeautifulSoup
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
	url = "http://www.hirunews.lk/sinhala/print-sinhala/" + id;
	print url

	#get html content from the url
	r  = requests.get(url)
	data = r.text

	#parse with BS
	soup = BeautifulSoup(data, "lxml")

	#get title
	h1s = soup.find_all("div", { "class" : "topic" })

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
	date = soup.find_all("span", { "class" : "createdate" })
	if len(date)<1 :
		print "An error occurred!"
		return
	date = date[0].get_text().strip()
	# convert date time to a common format
	# given -> Sunday, 28 May 2017 - 05:15 PM
	date = datetime.strptime(date, '%A, %d %B %Y - %I:%M %p')
	date = str(date)
	print date

	#get article content
	contents = soup.find_all("div", { "class" : "article" })
	contents = contents[0].get_text().strip()

	#save content to a file
	file = open("docs/hirunews_" + id + ".txt", "w") #
	file.write("<title>" + title.encode('utf8') + "</title>\n") 
	file.write("<time>" + date.encode('utf8') + "</time>\n") 
	#file.write("<author></author>\n") 
	file.write("<body>" + contents.encode('utf8') + "</body>") 
	file.close() 
	

	sql = "INSERT INTO `newsarticles` (`source`, `sid`, `time`, `title`, `body`) VALUES (%s, %s, %s, %s, %s);"
	
	try:
		cur.execute(sql, ('hirunews', id, date, title, contents))
		db.commit()
	except (MySQLdb.Error, MySQLdb.Warning), e:
		print "SQL Error"
		raise e
	

# scrap news items by id (from 2017/01/01 to present)
for n in range(151000, 162333):
	scrap(n)
	print "\n===============================\n\n"

	
db.commit()
db.close()