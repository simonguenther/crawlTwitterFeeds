import schedule
import time
from time import gmtime, strftime
from TwitterCrawler import Twitter_Crawler
from TelegramMemberCrawler import TelegramMemberCrawler
from RedditCrawler import RedditCrawler
import db
import Statistics

def ping(self):
	print str(strftime("%H:%M:%S", gmtime())) + ": alive!"

def save_to_file(text, filename):
	with open(filename+'.py', 'w') as file:
		file.write(text)

def create_report():
	reddit_error = Statistics.get_reddit_error_sites()
	twitter_error = Statistics.get_twitter_error_sites()

	output = "REPORT FOR "+time.strftime("%d/%m/%Y")+ "\n" \
			"\n===================================\n" \
 	    	 "Twitter Descriptions:\t " + str(Statistics.get_twitter_descriptions()) + "\n" \
			"Twitter Posts:\t\t " + str(Statistics.get_twitter_post()) + "\n\n" \
			"Reddit Descriptions:\t " + str(Statistics.get_reddit_descriptions()) + "\n" \
			"Reddit Posts:\t\t " + str(Statistics.get_reddit_post()) + "\n\n" \
			"Facebook Descriptions:\t " + str(Statistics.get_facebook_descriptions()) + "\n" \
			"Facebook Posts:\t\t " + str(Statistics.get_facebook_post()) + "\n\n" \
			"===================================\n" \
			"Twitter Errorlog: \n" \
			""+ Statistics.get_twitter_error_sites() + "\n" \
			"Reddit Errorlog: \n" \
			""+ Statistics.get_reddit_error_sites() + "\n" \
			"Facebook Errorlog: \n" \
			"" + Statistics.get_facebook_error_sites() + "\n"
	Statistics.reset_facebook()
	Statistics.reset_twitter()
	Statistics.reset_telegram()
	Statistics.reset_reddit()

	filename = time.strftime("%d-%m-%Y - Daily Social Media Report.txt")
	save_to_file(output,filename)
	print output

twitter = Twitter_Crawler()
telegram = TelegramMemberCrawler()
reddit = RedditCrawler()

schedule.every(10).minutes.do(create_report)
schedule.every(30).minutes.do(ping,0)
schedule.every(180).seconds.do(twitter.get_twitter_feeds)
schedule.every(180).seconds.do(reddit.get_reddit_posts)
schedule.every().day.at("00:01").do(twitter.get_description_information)
schedule.every().day.at("00:01").do(telegram.CrawlMembers)
schedule.every().day.at("00:01").do(reddit.get_reddit_general)
schedule.every().day.at("00:01").do(create_report)

while True:
	schedule.run_pending()
	time.sleep(1)
