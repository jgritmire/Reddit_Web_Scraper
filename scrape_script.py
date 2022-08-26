#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

#this video was IMMENSELY helpful https://www.youtube.com/watch?v=qhJ_gMB772U&ab_channel=TechPath

old_data = pd.read_csv('./data/reddit_data.csv')

ser = Service('chromedriver/chromedriver.exe')
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)


driver.get('https://www.reddit.com/')

# time.sleep(0.5)

post = driver.find_element_by_tag_name('body')

count = 0
while count < 500:
    post.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    count += 1

#Get the html and create a soup
html = driver.page_source

soup = BeautifulSoup(html)

#grabbing all posts
all_posts = soup.findAll('div',{'class':'_1oQyIsiPHYt6nx7VOmd1sz'})

# creating a list of dictionaries
current_time = datetime.datetime.now()

post_list = []
for post in all_posts:

    post_dict = {}
    try:
        #if this first line of code throws an error, post does not contain image, goes on to next block
        post.find('img',{'alt':'Post image'}).get('src')
        #append the relevant information to our list of dictionaries
        post_list.append({
        'id':post.get('id'),
        'title':post.find('h3', {'class':'_eYtD2XCVieq6emjKBH3m'}).text,
        'comments':post.find("span", {'class': 'FHCV02u6Cp2zYL0fhQPsO'}).text,
        'subreddit':(post.find('a', {'class':'_3ryJoIoycVkA88fy40qNJc'})).get('href'),
        'time':post.find('a',{'class':'_3jOxDPIQ0KaOWpzvSQo-1s'}).text,
        'upvotes':post.find('div', {'class':'_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo'}).text,
        'scraped_time':current_time,
        'contains_image':'1',
        'contains_video':'0',
        'text_only':'0'
        })
    except:
        try:
            #if this line of code throws an error, then post also does not contain video, goes on to next block
            post.find('video',{'class':'_1EQJpXY7ExS04odI1YBBlj'}).get('src')
            #append the relevant information to our list of dictionaries
            post_list.append({
            'id':post.get('id'),
            'title':post.find('h3', {'class':'_eYtD2XCVieq6emjKBH3m'}).text,
            'comments':post.find("span", {'class': 'FHCV02u6Cp2zYL0fhQPsO'}).text,
            'subreddit':(post.find('a', {'class':'_3ryJoIoycVkA88fy40qNJc'})).get('href'),
            'time':post.find('a',{'class':'_3jOxDPIQ0KaOWpzvSQo-1s'}).text,
            'upvotes':post.find('div', {'class':'_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo'}).text,
            'scraped_time':current_time,
            'contains_image':'0',
            'contains_video':'1',
            'text_only':'0'
            })
        except:
            try:
                #if THIS block of code throws an error, then the post is an ad, live stream, or live poll
                #append the relevant information to our list of dictionaries
                post_list.append({
                'id':post.get('id'),
                'title':post.find('h3', {'class':'_eYtD2XCVieq6emjKBH3m'}).text,
                'comments':post.find("span", {'class': 'FHCV02u6Cp2zYL0fhQPsO'}).text,
                'subreddit':(post.find('a', {'class':'_3ryJoIoycVkA88fy40qNJc'})).get('href'),
                'time':post.find('a',{'class':'_3jOxDPIQ0KaOWpzvSQo-1s'}).text,
                'upvotes':post.find('div', {'class':'_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo'}).text,
                'scraped_time':current_time,
                'contains_image':'0',
                'contains_video':'0',
                'text_only':'1'
                })
            except:
                pass

new_data = pd.DataFrame(post_list)

combined_df = pd.concat([old_data, new_data])

combined_df.to_csv('./data/reddit_data.csv', index = False)

driver.close()
