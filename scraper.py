import os
import psycopg2
import urllib2
import urlparse
import json
import datetime

# Connect to the database
# Needs DATABASE_URL environment variable defined. 
# For osx: export DATABASE_URL="postgres://mark@localhost/mark"
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])
conn_str = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(conn_str)
cur = conn.cursor()

# list of companies to save like counts for
companies = ["Starbucks","Oracle"] # could be pulled from database

# Like count the easy way. Not really scraping.
def likes_scrape_easy(company):
	return json.loads(urllib2.urlopen("https://graph.facebook.com/{}".format(company)).read())['likes']

# Actually scrape the page source.
def likes_scrape(company):
	pass # TODO

# Save the like count for a company. Log errors to the db.
def likes_save(company):

	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	try:
		likes = likes_scrape_easy(company) 
		#print "company = {}, likes = {}".format(company,likes)
		cur.execute("INSERT INTO casestudy_likes (time,company,num_likes) VALUES (%s,%s,%s)",(time,company,likes))
	except Exception, e:
		message =  "Error retrieving like count for {}. e={}".format(company,e)
		#print message
		cur.execute("INSERT into casestudy_logmessages (time,msg_text) VALUES (%s,%s)",(time,message))
	
	conn.commit()

# Save the like count for each company
for company in companies:
	likes_save(company)

conn.commit()
cur.close()
conn.close()
