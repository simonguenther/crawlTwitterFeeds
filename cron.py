import schedule
import time
from time import gmtime, strftime
from TwitterCrawler import Twitter_Crawler
from TelegramMemberCrawler import TelegramMemberCrawler
from RedditCrawler import RedditCrawler
import db

def ping(self):
	print str(strftime("%H:%M:%S", gmtime())) + ": alive!"

twitter = Twitter_Crawler()
telegram = TelegramMemberCrawler()
reddit = RedditCrawler()

schedule.every(30).minutes.do(ping)
schedule.every(180).seconds.do(twitter.get_twitter_feeds)
schedule.every(180).seconds.do(reddit.get_reddit_posts)
schedule.every().day.at("00:01").do(twitter.get_description_information)
schedule.every().day.at("00:01").do(telegram.CrawlMembers)
schedule.every().day.at("00:01").do(reddit.get_reddit_general)

while True:
	schedule.run_pending()
	time.sleep(1)
