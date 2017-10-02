import schedule
import time
from time import gmtime, strftime
import main
import db

def ping(self):
	print str(strftime("%H:%M:%S", gmtime())) + ": alive!"

schedule.every(30).minutes.do(ping,0)
schedule.every(30).seconds.do(main.get_twitter_feeds,0)
schedule.every().day.at("00:01").do(main.get_description_information,0)


while True:
	schedule.run_pending()
	time.sleep(1)
