# -*- coding: utf-8 -*-
"""
Created on Mon Jun 04 18:55:31 2018

@author: Hardik Galiawala
"""

import csv
import numpy as np
import re



dictionary = np.array([[]])

with open('lexicon_easy.csv', 'rb') as textfile:
    sentiWordNet = csv.reader(textfile, delimiter=',')
    for i in sentiWordNet:
        dictionary = np.append(dictionary, i[0].lower())
        dictionary = np.append(dictionary, i[1])
    dictionary = dictionary.reshape(len(dictionary)/2,2)

final_result = np.array([[]])

with open('tweetsUnencoded.csv', 'rb') as csvfile:
    tweet_unencoded = csv.reader(csvfile, delimiter=',')
    j = 0
    for tweet in tweet_unencoded:
        words = re.sub("[^\w]", " ",  tweet[-1]).split()
        score = np.array([])
        #print(words)
        for word in words:
            my_string="skewed#1 distorted#2"
            pattern = re.compile(r''+word.lower())
            for k in range(len(dictionary)):
                if(pattern.findall(dictionary[k][0]) != []):
                    score = np.append(score, dictionary[k][1])
                    break
        
        final_result = np.append(final_result, tweet[3])
        final_result = np.append(final_result, (np.sum(score.astype(int))))
    final_result = final_result.reshape(len(final_result) / 2, 2)
    

with open('sentimentAnalysis.csv', 'wb') as outfile:
    
    writer = csv.writer(outfile)
    writer.writerow(['twitter tweet', 'sentiment', 'score'])
    for count in range(len(final_result)):
        
        sentiment = ""
        if (int(final_result[count][1]) > 0):
            sentiment = "Positive"
        elif(int(final_result[count][1]) < 0):
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        writer.writerow([final_result[count][0], sentiment, final_result[count][1]])
