# -*- coding: utf-8 -*-
"""
Created on Sat Jun 02 13:09:54 2018

@author: Hardik Galiawala
"""

import tweepy
import time
import csv
import json
import numpy as np
import pandas as pd
import re

# Consumer and access key can be added below. Removed for security reasons.

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


# Establish connection

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


# Remove emojis
# Reference: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python#33417311
def discard_emoji(tweet_text):
    
    emojis_removed = re.compile(u"[^\U00000000-\U0000d7ff\U0000e000-\U0000ffff]", flags=re.UNICODE)
    return emojis_removed.sub(u'', unicode(tweet_text, 'utf-8'))
    

def get_profile(screen_name):
    api = tweepy.API(auth)
    try:
    #https://dev.twitter.com/rest/reference/get/users/show describes
        user_profile = api.get_user(screen_name)
    except tweepy.error.TweepError as e:
        user_profile = json.loads(e.response.text)
    return user_profile


def get_trends(location_id):
    api = tweepy.API(auth)
    try:
        trends = api.trends_place(location_id)
    except tweepy.error.TweepError as e:
        trends = json.loads(e.response.text)
    
    return trends

def get_tweets_lab(query):
    api = tweepy.API(auth)
    try:
        tweet = api.search(query, count = 30)
    except tweepy.error.TweepError as e:
        tweet = json.loads(e.response.text)
    
    return tweet

tweet_details = np.array([])
tweet_user = np.array([])
tweet_id_str = np.array([])
created_at = np.array([])

queries = ["#HanSolo -filter:retweets lang:en"," \"Nova Scotia\"","@Windows filter:retweets lang:en", "#realDonaldTrump filter:retweets lang:en"]

with open('tweetsUnencoded.csv', 'wb') as outfile:
    
    writer = csv.writer(outfile)
    #writer.writerow(['id', 'user', 'created_at', 'text'])
    for query in queries:
        t = get_tweets_lab(query)
        for tweet in t:
            
            
            hashtags = re.sub(r'#\S+', '', tweet.text.encode('utf-8'))
            tags = re.sub(r'@\S+', '', hashtags)
            url = re.sub(r'http\S+', '', tags)
            retweet = re.sub(r'RT ', '', url)
            retweet_emoji = discard_emoji(retweet)
            writer.writerow([tweet.id_str, tweet.user.screen_name, 
                             tweet.created_at, retweet_emoji.encode('ascii', errors = 'ignore')])
