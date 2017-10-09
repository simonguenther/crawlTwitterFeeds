
count_twitter_posts = 0
count_twitter_descriptions = 0

count_reddit_posts = 0
count_reddit_descriptions = 0

count_facebook_posts = 0
count_facebook_descriptions = 0

twitter_error_sites = []
reddit_error_sites = []
telegram_error_sites = []
facebook_error_sites = []

""" REDDIT """

def inc_reddit_post():
    global count_reddit_posts
    count_reddit_posts += 1

def inc_reddit_descriptions():
    global count_reddit_descriptions
    count_reddit_descriptions += 1

def add_reddit_error_sites(site):
    global reddit_error_sites
    reddit_error_sites.append(site)

def get_reddit_error_sites():
    global reddit_error_sites
    if len(reddit_error_sites) == 0:
        return ""
    else:
        return "\n".join(reddit_error_sites)

def get_reddit_post():
    global count_reddit_posts
    return count_reddit_posts

def get_reddit_descriptions():
    global count_reddit_descriptions
    return count_reddit_descriptions

def reset_reddit():
    global count_reddit_descriptions
    global count_reddit_posts
    global reddit_error_sites
    count_reddit_descriptions = 0
    count_reddit_posts = 0
    reddit_error_sites = []

""" TWITTER """

def inc_twitter_post():
    global count_twitter_posts
    count_twitter_posts += 1

def inc_twitter_descriptions():
    global count_twitter_descriptions
    count_twitter_descriptions += 1

def get_twitter_post():
    global count_twitter_posts
    return count_twitter_posts

def get_twitter_descriptions():
    global count_twitter_descriptions
    return count_twitter_descriptions

def add_twitter_error_sites(site):
    global twitter_error_sites
    twitter_error_sites.append(site)

def get_twitter_error_sites():
    global twitter_error_sites
    if len(twitter_error_sites) == 0:
        return ""
    else:
        return "\n".join(twitter_error_sites)

def reset_twitter():
    global count_twitter_descriptions
    global count_twitter_posts
    global twitter_error_sites
    count_twitter_descriptions = 0
    count_twitter_posts = 0
    twitter_error_sites = []

""" TELEGRAM """

def add_telegram_error_sites(site):
    global telegram_error_sites
    telegram_error_sites.append(site)

def get_telegram_error_sites():
    global telegram_error_sites
    if len(telegram_error_sites) == 0:
        return ""
    else:
        return "\n".join(telegram_error_sites)

def reset_telegram():
    global telegram_error_sites
    telegram_error_sites = []

""" FACEBOOK """

def inc_facebook_post():
    global count_facebook_posts
    count_facebook_posts += 1

def inc_facebook_descriptions():
    global count_facebook_descriptions
    count_facebook_descriptions += 1

def get_facebook_post():
    global count_facebook_posts
    return count_facebook_posts

def get_facebook_descriptions():
    global count_facebook_descriptions
    return count_facebook_descriptions

def add_facebook_error_sites(site):
    global facebook_error_sites
    facebook_error_sites.append(site)

def get_facebook_error_sites():
    global facebook_error_sites
    if len(facebook_error_sites) == 0:
        return ""
    else:
        return "\n".join(facebook_error_sites)

def reset_facebook():
    global count_facebook_descriptions
    global count_facebook_posts
    global facebook_error_sites
    count_facebook_descriptions = 0
    count_facebook_posts = 0
    facebook_error_sites = []
