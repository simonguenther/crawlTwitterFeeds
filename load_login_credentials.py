import json
import collections

class Login:

    credentials = ""
    path = 'login_credentials.json'

    @staticmethod
    def load_credentials():
        with open (Login.path) as data_file:
            try:
                Login.credentials = json.load(data_file)
            except StandardError as e:
                print "Error when loading credentials from file! " + str(e)
    
    @staticmethod
    def get_twitter_credentials():
        Login.load_credentials()
        twitter_logins = Login.credentials["Twitter"]
        count_logins = len(twitter_logins)
        if count_logins > 1:
            raise "Too many Twitter login credentials found"
        for x in twitter_logins:
            return twitter_logins[x]


    @staticmethod
    def get_reddit_credentials ():
        Login.load_credentials()
        reddit_logins = Login.credentials["Reddit"]
        count_logins = len(reddit_logins)
        if count_logins > 1:
            raise "Too many Reddit login credentials found"
        for x in reddit_logins:
            return reddit_logins[x]


    @staticmethod
    def get_facebook_credentials ():
        Login.load_credentials()
        facebook_logins = Login.credentials["Facebook"]
        count_logins = len(facebook_logins)
        if count_logins > 1:
            raise "Too many Facebook login credentials found"
        for x in facebook_logins:
            return facebook_logins[x]

            


