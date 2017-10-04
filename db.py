import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
import psycopg2
import re


def open_connection():
	conn = psycopg2.connect(database="projects_data", user = "postgres", password = "postgrespass", host = "127.0.0.1", port = "5432")
	#print "database successfully opened"
	return conn

"""#########"""
""" TWITTER """
"""#########"""
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

"""##########"""
""" TELEGRAM """
"""##########"""

def get_telegram_urls(conn):
	query = "SELECT symbol, telegram_ann FROM projects_main WHERE telegram_ann != ''"
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	handles = {}
	if rows and len(rows)>0:
		for row in rows:
			handles[row[0]] = row[1]
	return handles

def insert_in_telegram_general(conn,telegram_general_obj):
	query = "INSERT INTO telegram_general (symbol, telegram_members, time_lookup) \
		VALUES ('%s','%s','%s' )" % (telegram_general_obj["symbol"],telegram_general_obj["members"], telegram_general_obj["time_lookup"])
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()

"""##########"""
""" REDDIT """
"""##########"""


def get_reddit_urls(conn):
	query = "SELECT reddit FROM projects_main WHERE reddit != ''"
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	handles = []
	if rows and len(rows)>0:
		for row in rows:
			handles.append(row[0])
	return handles

def insert_in_reddit_handle_info(conn,reddit_general_obj):
	query = "INSERT INTO reddit_general (id,name,count_readers,information,time_creation,moderators,time_lookup) \
      VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (reddit_general_obj["id"],reddit_general_obj["name"],reddit_general_obj["count_readers"],reddit_general_obj["information"],reddit_general_obj["time_creation"],reddit_general_obj["moderators"],reddit_general_obj["time_lookup"])
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()

def check_is_reddit_post_exists(conn,post_id):
	post_exists = False
	query = "SELECT * FROM reddit_posts where id='%s'" % post_id
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	if rows and len(rows)>0:
		post_exists = True
	return post_exists

def insert_in_reddit_post(conn,reddit_general_obj):
	if check_is_reddit_post_exists(conn,reddit_general_obj["id"]) == False:
		query = "INSERT INTO reddit_posts (id,name,title,url_post,url_comments,poster,timestamp,time_lookup) \
	      VALUES ('%s','%s','%s','%s','%s','%s','%s','%s' )" % (reddit_general_obj["id"],reddit_general_obj["name"],reddit_general_obj["title"],reddit_general_obj["url_post"],reddit_general_obj["url_comments"],reddit_general_obj["poster"],reddit_general_obj["timestamp"],reddit_general_obj["time_lookup"])
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()
