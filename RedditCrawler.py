import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
import praw
from db import insert_in_reddit_handle_info,insert_in_reddit_post,open_connection, get_reddit_urls
import json
import datetime
import Statistics
from time import gmtime, strftime

class RedditCrawler:
    username = 'bhvi'
    password = '!1Bhavya'
    client_id = 'O0oy5piyZ9HxFA'
    client_secret = 'xgx_MidZbfC9jc8HkN2xc5Qk4BU'
    UA = 'Over 9000 Bot by /u/bhvi'

    conn = open_connection()

    r = praw.Reddit(username = username,
                password = password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = UA)

    user_handle_list = get_reddit_urls(conn)
    
    def get_reddit_general(self):
        try:
            print str(strftime("%H:%M:%S", gmtime())) + ": Checking Reddit Genereal!"
            for user_handle in self.user_handle_list:
                subreddit_obj = self.r.subreddit(user_handle)
                reddit_general_obj = {}
                reddit_general_obj["id"] = subreddit_obj.id
                reddit_general_obj["count_readers"] = subreddit_obj.subscribers
                reddit_general_obj["name"] = subreddit_obj.display_name
                reddit_general_obj["information"] = subreddit_obj.description.replace("'","")
                moderator_str = ""
                for moderator in subreddit_obj.moderator():
                    moderator_str += ","+str(moderator)
                reddit_general_obj["moderators"] = moderator_str
                reddit_general_obj["time_lookup"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                reddit_general_obj["time_creation"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_in_reddit_handle_info(self.conn,reddit_general_obj)
                Statistics.inc_reddit_descriptions()
        except StandardError as e:
            Statistics.add_reddit_error_sites(user_handle + "\t" + str(e))
            #print "[get_reddit_general()-ERROR at " + str(user_handle) + "\n"+str(e)

    def get_reddit_posts(self):
        try:
            print str(strftime("%H:%M:%S", gmtime())) + ": Checking Reddit Posts!"
            for user_handle in self.user_handle_list:
                subreddit_obj = self.r.subreddit(user_handle)
                for submission in subreddit_obj.hot(limit=100):
                    epoch = datetime.datetime.utcfromtimestamp(int(submission.created_utc))
                    reddit_post_obj = {}
                    reddit_post_obj["url_post"] = submission.url
                    """ Bug needs to be fixed """
                    """if(submission.url == "https://www.sec.gov/news/press-release/2017-184"):
                        print subreddit_obj
                        break"""
                    reddit_post_obj["id"] = submission.id
                    # Check if username is available or deleted
                    hasName = getattr(submission,"name",None)
                    if hasName:
                        reddit_post_obj["name"] = submission.name    
                    else:
                        reddit_post_obj["name"] = "[deleted]"
                    
                    # Check if author is availabe or deleted
                    hasAuthor = getattr(submission,"name",None)
                    if hasAuthor:
                        reddit_post_obj["poster"] = submission.author.name
                    else: 
                        reddit_post_obj["poster"] = "[deleted]"
                    
                    reddit_post_obj["title"] = submission.title.replace("'","")
                    reddit_post_obj["url_comments"] = "https://www.reddit.com/r/"+user_handle+"/comments/"+submission.id
                    reddit_post_obj["time_lookup"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    reddit_post_obj["timestamp"] = epoch.strftime("%Y-%m-%d %H:%M:%S")

                    insert_in_reddit_post(self.conn,reddit_post_obj)
                    Statistics.inc_reddit_post()
                    #print reddit_post_obj
                    # break
        except StandardError as e:
            Statistics.add_reddit_error_sites(user_handle + "\t" + str(e))
            #print "[get_reddit_posts()-ERROR at " + str(user_handle) + " @ " + submission.url + "\n"+str(e)