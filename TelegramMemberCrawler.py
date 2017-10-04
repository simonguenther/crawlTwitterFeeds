import sys
reload(sys) 
import time
from time import gmtime, strftime
sys.setdefaultencoding( "utf-8" )
import datetime
from db import open_connection, get_telegram_urls,insert_in_telegram_general
import urllib
from bs4 import BeautifulSoup

class TelegramMemberCrawler:
    def CrawlMembers(self):
        conn = open_connection()
        user_handle_list = get_telegram_urls(conn)
        print str(strftime("%H:%M:%S", gmtime())) + ": Checking Telegram!"
        error_links = []
        
        for user_handle in user_handle_list:
            #print "Analyzing: "+ user_handle
            htmltext = urllib.urlopen(user_handle_list[user_handle]).read()
            soup = BeautifulSoup(htmltext, "lxml")
            first = soup.find("div", {"class":"tgme_page_extra"})
            if first is not None:
                member_count = first.text.split()[0].strip()
                pair = {}
                pair["symbol"] = user_handle
                pair["members"] = member_count
                pair["time_lookup"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_in_telegram_general(conn, pair)
                #print "Analyzing: "+ user_handle + " @ " + str(member_count)
            else:
                error_links.append(user_handle)
        print "Telegram error_sites:"
        print error_links

