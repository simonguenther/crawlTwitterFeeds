import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
import tweepy
from db import insert_in_twitter_feed,insert_in_handle_info,open_connection, get_twitter_urls
import json
import datetime


consumer_key = "TlyIHECSh3WWhlAE4kTZH8uzv"
consumer_secret = "qM8DtIrkirjgY5BcX89lvXtk2kEUK1lXg3uVPCXGof5AVvxmgh"
access_token = "912399918030974976-yIrqxPadAImudCU6KtX28xhUx3p7eiz"
access_token_secret = "znXnm4JteceK3FLmrPzmTr2szEUvVYMjHVfgyUr8hsjVI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

conn = open_connection()
user_handle_list = get_twitter_urls(conn)

for user_handle in user_handle_list:
	other_tweets = api.user_timeline(user_handle,count=20)
	t = 1
	for tweet in other_tweets:
		# print dir(tweet)
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
			print t,": id:",tweet.id_str," :",tweet.text.encode("utf-8")
		t = t+1
		# break

	user = api.get_user(user_handle)
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

conn.close()