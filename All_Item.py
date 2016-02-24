import requests
import base64
import sys, os
import re
from bs4 import BeautifulSoup

YAHOO_BASE_URL = 'https://tw.buy.yahoo.com'

def get_yahoo_title():
  yahoo_request_url = "https://tw.buy.yahoo.com/help/helper.asp?p=sitemap"
  yahoo_resp = requests.get(yahoo_request_url)
  yahoo_resp.encoding='big5'
  soup = BeautifulSoup(yahoo_resp.text, "lxml")
  content = soup.find("div", attrs = {'class' : 'content'})
  for zone in content.find_all(class_ = re.compile("zone")):
    title     = zone.a.string
    title_url = YAHOO_BASE_URL + zone.a.get('href')
    for site_list in zone.select(".site-list"):
      cat_title     = site_list.a.string
      cat_title_url = YAHOO_BASE_URL + site_list.a.get('href') 


def get_item_info(url):
  item_resp = requests.get(url)
  item_resp.encoding = 'utf-8'
  soup = BeautifulSoup(item_resp.text, "lxml")

  item_spec = soup.find(class_ = re.compile("item-spec"))
  subtitle       = item_spec.find(class_ = "subtitle").string
  title          = item_spec.find(class_ = "title").text + subtitle
  item_desc_list = item_spec.find(class_ = re.compile("desc-list")).text.strip("\r\n ").split("\n")
  suggest_price  = item_spec.find(class_ = "suggest").text.strip("\r\n ")
  special_price  = "特價" + item_spec.find(class_ = "priceinfo").text.strip("\r\n ")

  desc = list()
  for s in item_desc_list:
    desc.append("*" + s)

  print(title)
  print("\n".join(desc))
  print(suggest_price)
  print(special_price)
  

def main():
  url = 'https://tw.buy.yahoo.com/gdsale/%E5%BE%B7%E5%9C%8B%E9%BA%A5%E5%A4%A7%E5%B8%AB-Mestemacher%E5%A4%A9%E7%84%B6-%E4%BB%80%E9%8C%A6%E7%A9%80%E7%89%871-6358385.html'
  get_item_info(url)

main()
