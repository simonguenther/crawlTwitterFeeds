import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
from db import insert_in_facebook_post,insert_in_facebook_handle_info,open_connection, check_is_facebook_post_exists, get_facebook_urls
from load_login_credentials import Login
import json
import facebook
import datetime
import time
import Statistics

class FacebookCrawler:
    facebook_credentials = Login.get_facebook_credentials()
    graph = facebook.GraphAPI(access_token=facebook_credentials["access_token"], version="2.10")

    conn = open_connection()
    user_handle_list = get_facebook_urls(conn)

    """ 

		Extract description info from facebook profile

	"""
    def get_description_information(self):
        for user_handle in self.user_handle_list:
            try:
                site_info = self.graph.get_object(id=user_handle,fields="id,name,fan_count,rating_count,website,overall_star_rating,username")
                facebook_general_obj = {}
                facebook_general_obj["id"] = site_info.get("id","")
                facebook_general_obj["handle"] = site_info.get("username","")
                facebook_general_obj["name"] = site_info.get("name","")
                if site_info.get("overall_star_rating","") is "":
                    facebook_general_obj["rating"] = 0
                else:
                    facebook_general_obj["rating"] = site_info.get("overall_star_rating","")

                if site_info.get("rating_count","") is "":
                    facebook_general_obj["count_reviews"] = 0
                else:    
                    facebook_general_obj["count_reviews"] = site_info.get("rating_count","")

                if site_info.get("fan_count","") is "":
                    facebook_general_obj["count_likes"] = 0
                else:
                    facebook_general_obj["count_likes"] = site_info.get("fan_count","")

                facebook_general_obj["count_followers"] = 0
                facebook_general_obj["time_lookup"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                facebook_general_obj["url"] = "https://www.facebook.com/"+site_info.get("username","")
                insert_in_facebook_handle_info(self.conn,facebook_general_obj)
                
            except StandardError as e:
                #print user_handle + "\t" + str(e)
                Statistics.add_facebook_error_sites(user_handle + "\t" + str(e))
            except facebook.GraphAPIError as e:
                #print user_handle + "\t" + str(e)
                Statistics.add_facebook_error_sites(user_handle + "\t" + str(e))

	"""

		Get all facebook posts which are not already in the database

	"""
    def get_facebook_posts(self):
        for user_handle in self.user_handle_list:

            try:
                posts_info = self.graph.get_object(id=user_handle+"/posts")
                post_list = posts_info.get("data",[])
                
                for post in post_list:
                    facebook_post_obj = {}
                    facebook_post_obj["id"] = post.get("id","")
                    facebook_post_obj["url"] = ""	
                    facebook_post_obj["handle"] = user_handle
                    facebook_post_obj["content"] = post.get("message","").replace("'","")
                    facebook_post_obj["timestamp"] = post.get("created_time","")
                    facebook_post_obj["time_lookup"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    insert_in_facebook_post(self.conn,facebook_post_obj)
                    #print(facebook_post_obj["id"],":...inserted")
            except StandardError as e:
            #    print user_handle + "\t" + str(e)
                Statistics.add_facebook_error_sites(user_handle + "\t" + str(e))
            except facebook.GraphAPIError as e:
                #print user_handle + "\t" + str(e)
                Statistics.add_facebook_error_sites(user_handle + "\t" + str(e))
        
            