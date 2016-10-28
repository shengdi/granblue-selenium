# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

#Gets raid ID for lvl 60 leviathan omega
def get_raid_id():
  r = requests.get('https://twitter.com/search?f=tweets&vertical=default&q=Lv60%20%E3%83%AA%E3%83%B4%E3%82%A1%E3%82%A4%E3%82%A2%E3%82%B5%E3%83%B3%E3%83%BB%E3%83%9E%E3%82%B0%E3%83%8A')
  soup = BeautifulSoup(r.text, 'html.parser')
  first = soup.find_all(class_="TweetTextSize")[0]
  eid = first.text.split('\n')[0].split(u'\uff1a')[1]
  return eid
#Get one id to try:

def get_bahamut_id():
  r = requests.get('https://twitter.com/search?f=tweets&vertical=default&q=Lv100%20プロトバハムート')
  soup = BeautifulSoup(r.text, 'html.parser')
  first = soup.find_all(class_="TweetTextSize")[0]
  eid = first.text.split('\n')[0].split(u'\uff1a')[1]
  return eid