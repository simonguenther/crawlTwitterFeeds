import sys
reload(sys) 
import time
from time import gmtime, strftime
sys.setdefaultencoding( "utf-8" )
import tweepy
from db import insert_in_twitter_feed,insert_in_handle_info,open_connection, get_twitter_urls
import json
import datetime
import Statistics

class Twitter_Crawler:
	""" Tweepy API Settings """
	consumer_key = "USDOh2a9f8Z1PBXfbAmkSBxEC"
	consumer_secret = "LCDyTtrItqwJ9S4nAwZffarzeqyjOE4anZhxs7y3aMAhW60ZB4"
	access_token = "911961422791397376-EzE65iS50Xs4zp6rOvd2b11px8l5WTJ"
	access_token_secret = "1lVLwmY3evpa7dpVE60h4Im0j1Yx3FwJlZExrjqIDIxyp"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	""" 

		Extract description info from twitter profile

	"""
	def get_description_information(self):
		print str(strftime("%H:%M:%S", gmtime())) + ": Checking Description!"
		conn = open_connection()
		user_handle_list = get_twitter_urls(conn)
		error_sites = []
		try:
			for user_handle in user_handle_list:
				print "Checking " + user_handle
				user = self.api.get_user(user_handle)
				twitter_general_obj = {}
				twitter_general_obj["join_date"] = user.created_at
				twitter_general_obj["description"] = user.description
				twitter_general_obj["handle"] = user.screen_name
				twitter_general_obj["name"] = user.name
				twitter_general_obj["tweetcount"] = user.statuses_count
				twitter_general_obj["followercount"] = user.followers_count
				twitter_general_obj["location"] = user.location
				twitter_general_obj["desc_link"] = user.url
				twitter_general_obj["time_lookup"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				insert_in_handle_info(conn,twitter_general_obj)
				Statistics.inc_twitter_descriptions()
		except StandardError as e:
			Statistics.add_twitter_error_sites(user_handle + "\t" + str(e))
			#error_sites.append(user_handle)
		except tweepy.TweepError as e:
			#message = str(e.message[0]['code']) + "\n" + str(e.args[0][0]['code'])
			Statistics.add_twitter_error_sites(user_handle + "\t" + str(e.message))
		conn.close()
		#print error_sites
	"""

		Get all twitter posts which are not already in the database

	"""
	def get_twitter_feeds(self):
		print str(strftime("%H:%M:%S", gmtime())) + ": Checking Twitter feeds!"
		conn = open_connection()

		# Retrieve twitter handles from main database
		user_handle_list = get_twitter_urls(conn)
		error_sites = []

		# Retrieve posts for every handle
		for user_handle in user_handle_list:
			print "Checking " + user_handle 
			try:
				other_tweets = self.api.user_timeline(user_handle,count=100)
				for tweet in other_tweets:
					if tweet.in_reply_to_status_id_str is not None:
						continue
					# print "retweet_from_handle: ",tweet.retweeted
					# print "in_reply_to_status_id_str: ",tweet.in_reply_to_status_id_str
					account = tweet.user.screen_name
					source_url = "https://twitter.com/"+tweet.user.screen_name+"/status/"+tweet.id_str
					content = tweet.text.replace("'","").encode("utf-8")
					timstamp = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
					time_lookup = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					retweet_from_handle = tweet.author.screen_name
					twitter_feed_obj = {}
					twitter_feed_obj["account"] = account
					twitter_feed_obj["url"]  = source_url
					twitter_feed_obj["content"] = content
					twitter_feed_obj["timestamp"] = timstamp
					twitter_feed_obj["time_lookup"] = time_lookup
					if tweet.retweeted:
						twitter_feed_obj["retweet_from_handle"] = retweet_from_handle
					else:
						twitter_feed_obj["retweet_from_handle"] = ""
					if insert_in_twitter_feed(conn,twitter_feed_obj):
						Statistics.inc_twitter_post()
						print "New feed found @ " + account
			except StandardError as e:
				Statistics.add_twitter_error_sites(user_handle + "\t" + str(e))
				#error_sites.append(user_handle)
			except tweepy.TweepError as e:
				#message = str(e.message[0]['code']) + "\n" + str(e.args[0][0]['code'])
				Statistics.add_twitter_error_sites(user_handle + "\t" + str(e.message))
				#error_sites.append(user_handle)

		#print error_sites
		conn.close()

		