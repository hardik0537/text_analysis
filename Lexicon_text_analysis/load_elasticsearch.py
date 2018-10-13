# -*- coding: utf-8 -*-
"""
Created on Wed Jun 06 15:13:45 2018

@author: Hardik Galiawala
"""

import csv
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, connections

connections.create_connection(hosts=['team1.canadaeast.cloudapp.azure.com'])

class Tweet(DocType):
    #user = Text(analyzer='snowball', fields={'raw': Keyword()})
    tweet = Text(analyzer='snowball')
    score = Text()
    sentiment = Text(analyzer='snowball')
    #hashtags = Keyword()
    created_at = Date()
    
    class Meta:
        index = 'tweet_sentiments'
        
        def save(self, ** kwargs):
            '''
            self.lines = len(self.tweet.split())
            self.hashtags = [tag for tag in 
                                 self.tweet.split() 
                                 if tag.startswith('#')]
            '''
            return super(Tweet, self).save(** kwargs)
        
with open('sentimentAnalysis.csv', 'rb') as csvfile:
    
    id_number = 0
    sentiment = csv.reader(csvfile, delimiter=',')
    for i in sentiment:

        id_number = id_number + 1
        Tweet.init()
        tweet = Tweet(meta={'id': id_number})
        tweet.tweet = i[0]
        tweet.sentiment = i[1]
        tweet.score = i[2]
        tweet.created_at = datetime.now()
        tweet.save()
    

