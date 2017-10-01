import schedule
import time
from time import gmtime, strftime
import main
import db

def ping(self):
	print str(strftime("%H:%M:%S", gmtime())) + ": alive!"

def activateGlobalTracking(self):
	print "Global Snapshot activated! Save general info from every Twitter feed"
	main.snapshot_global = True

schedule.every(30).minutes.do(ping,0)
schedule.every(30).seconds.do(main.run,0)
schedule.every(1).day.do(activateGlobalTracking,0)

while True:
	schedule.run_pending()
	time.sleep(1)
