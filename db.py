import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
import psycopg2
import re


def open_connection():
	conn = psycopg2.connect(database="projects_data", user = "postgres", password = "postgrespass", host = "127.0.0.1", port = "5432")
	#print "database successfully opened"
	return conn

def insert_in_handle_info(conn,twitter_general_obj):
	query = "INSERT INTO twitter_general (join_date,description,handle,name,tweetcount,followercount,location,desc_link,time_lookup) \
      VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s' )" % (twitter_general_obj["join_date"],twitter_general_obj["description"].replace("'","''"),twitter_general_obj["handle"],twitter_general_obj["name"],twitter_general_obj["tweetcount"],twitter_general_obj["followercount"],twitter_general_obj["location"],twitter_general_obj["desc_link"],twitter_general_obj["time_lookup"])
	cur = conn.cursor()
	query = cur.mogrify(query)
	cur.execute(query)
	conn.commit()

def check_is_feed_exists(conn,feed_url):
	feed_exists = False
	query = "SELECT * FROM twitter_feed where url='%s'" % feed_url
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	if rows and len(rows)>0:
		feed_exists = True
	return feed_exists

def insert_in_twitter_feed(conn,twitter_general_obj):
	if check_is_feed_exists(conn,twitter_general_obj["url"]) == False:
		query = "INSERT INTO twitter_feed (account,url,content,timestamp,time_lookup,retweet_from_handle) \
	      VALUES ('%s','%s','%s','%s','%s','%s' )" % (twitter_general_obj["account"],twitter_general_obj["url"],twitter_general_obj["content"].replace("'","''"),twitter_general_obj["timestamp"],twitter_general_obj["time_lookup"],twitter_general_obj["retweet_from_handle"])
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()
		return True
	return False

def get_twitter_urls(conn):
	query = "SELECT twitter FROM projects_main"
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	handles = []
	if rows and len(rows)>0:
		for row in rows:
			if row[0] != "":
				handles.append(row[0].strip("@"))
	return handles
# open_connection()