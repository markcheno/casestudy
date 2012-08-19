import os
import psycopg2
import urllib2
import urlparse
import json
import datetime
import re

#
# Connect to the database (postgres, herkou friendly)
# Needs DATABASE_URL environment variable defined. 
# For osx: export DATABASE_URL="postgres://mark@localhost/mark"
#
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])
conn_str = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(conn_str)
cur = conn.cursor()

#
# list of companies to save like counts for
#
companies = ["Starbucks","Oracle"] # could be pulled from database

#
# Like count the easy way. Use the facebook graph api. Not really scraping.
#
def likes_scrape_easy(company):
	return json.loads(urllib2.urlopen("https://graph.facebook.com/{}".format(company)).read())['likes']

#
# Actually scrape the page source. Grab the raw html and then use a regular expression to find 
# the first occurrence of a number (possibly containing commas) followed by one or more spaces, 
# then the text "likes". This is prone to breakage if the facebook page changes it's layout
# significantly. It is also much more resource intensive compared to using the facebook graph api. 
#
def likes_scrape(company):
	html = urllib2.urlopen("http://www.facebook.com/{}".format(company)).read()
	likes_text = re.search("(((\d{1,3})(,\d{3})*)|(\d+))(\s*likes)",html).groups()[0]
	return likes_text.replace(",","")

#
# Save the like count for a company. Log errors to the db. Could also generate an email on an error.
#
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

#
# Save the like count for each company
#
for company in companies:
	likes_save(company)

cur.close()
conn.close()
