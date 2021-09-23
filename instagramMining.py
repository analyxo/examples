# -*- coding: utf-8 -*-
"""
Created on Dec  28 18:55:26 2020
Updated on Sep 22 23:11:24 2021
@author: Dr. Emanuel Christner
Interested in potential of comprehensive customer resonance monitoring and
AI-based drilldown analyses?
Just give as a call: www.aspectivo.ai
"""

#This script gives you an idea how simple keyword monitoring and
#semantic baseline assessment of social media content from channels
#such as instagram is.
#To get a more nuanced picture, you can start from this point and
#drill down with more advanced NLP technologies.

#import libraries
import instaloader
import pandas as pd
from langdetect import detect
import langdetect
langdetect.DetectorFactory.seed = 0
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#specifiy what keywords you're interested in
brand=['adidas', 'fashion']

#get posts
#you can interrupt this loop once enough content has been collected.
#getting error 'Redirected to login page. Use --login'? ->Check 'request balancer'.
loader = instaloader.Instaloader()
insta_df = pd.DataFrame(columns=['timestamp','text','likes','comments'])
for post in loader.get_hashtag_posts(brand[0]):
    if len(post._node['edge_media_to_caption']['edges']) > 0:
        content = post._node['edge_media_to_caption']['edges'][0]['node']['text']
        if brand[1] in content:
            likes = post._node['edge_liked_by']['count']
            comments = post._node['edge_media_to_comment']['count']
            timestamp = post.date
            insta_df = insta_df.append(pd.DataFrame([[timestamp, content, likes, comments]], columns=['timestamp','text','likes','comments']), ignore_index=True)  
            print(timestamp)
    
#determine langugages of posts
def detect_lang(sentence):
    try:
        return detect(sentence.lower())
    except:
        return None
insta_df['lang'] = insta_df['text'].map(lambda x: detect_lang(x))

#select english posts
df_instagram = insta_df.copy(deep=True)
df_instagram = df_instagram[df_instagram.lang == 'en']

#analyze sentiment
analyzer = SentimentIntensityAnalyzer()
df_instagram['sentiment'] = df_instagram['text'].apply(lambda x: analyzer.polarity_scores(x)).apply(pd.Series)['compound']

#Really simple, isn't it? Have fun digging deeper!