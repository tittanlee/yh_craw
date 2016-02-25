import requests
import base64
import sys, os
import re
import math
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
      sub_title     = site_list.a.string
      sub_title_url = YAHOO_BASE_URL + site_list.a.get('href') 

def get_yahoo_category(yahoo_cate_url):
  yahoo_cate_url = 'https://tw.buy.yahoo.com/?sub=114'
  yahoo_resp = requests.get(yahoo_cate_url)
  yahoo_resp.encoding = "utf-8"
  soup = BeautifulSoup(yahoo_resp.text, "lxml")
  cate_menu = soup.find("div", attrs = {'id' : 'cl-menucate'})
  stitle_url = ""
  for site_list in cate_menu.find_all(attrs = {'class' :"sitelist"}):
    for cate_stitle in site_list.select(".stitle"):
      stitle     = cate_stitle.get_text().strip("\r\n ")
      try:
        stitle_url = cate_stitle.a.get('href')
        print("%s %s" %(stitle, stitle_url))
      except:
        print("%s" %(stitle))
        break

    for cate_list in site_list.select(".list"):
      cate_name = cate_list.a.get_text()
      cate_url  = cate_list.a.get('href')
      print(" |- %s %s" %(cate_name, cate_url))

def get_yahoo_item(yahoo_cate_item_url):
  yahoo_cate_item_url = 'https://tw.buy.yahoo.com/?catitemid=97524'
  # page_dict = get_paging_dict(yahoo_cate_item_url)

  yahoo_resp = requests.get(yahoo_cate_item_url )
  yahoo_resp.encoding = "utf-8"
  soup = BeautifulSoup(yahoo_resp.text, "lxml")
  for recommend_item in soup.find_all("div", attrs = {'class' : re.compile('pdlsit-main')}):
    rec_item_name = recommend_item.select(".name")
    print(rec_item_name.a)
    # rec_item_url  = recommend_item.a.get('href')
    # print("%s %s" %(rec_item_name, rec_item_url))
  
def get_paging_dict(yahoo_cate_item_url):
  yahoo_resp = requests.get(yahoo_cate_item_url )
  yahoo_resp.encoding = "utf-8"
  soup = BeautifulSoup(yahoo_resp.text, "lxml")
  count_of_item = soup.find("div", attrs = {'id' : 'cl-pagination'})
  count_of_item = count_of_item.find("div", attrs = {'class' : re.compile('summary')})
  total_page = count_of_item.string.strip().replace(" ","")
  total_page = int(list(filter(None, re.split('\D+', total_page)))[-1])

  ITEMS_IN_EACH_PAGE = 24
  page_data = dict()
  page_dict = {'paging':page_data}
  page_count = math.ceil(total_page / ITEMS_IN_EACH_PAGE) + 1
  for page in range(1, page_count):
    item_url = ("%s&page=%d&order=0" %(yahoo_cate_item_url, page))
    page_data[page] = item_url

  return page_dict

    
    
def get_detail_item_info(yahoo_item_url):
  item_resp = requests.get(yahoo_item_url)
  item_resp.encoding = 'utf-8'
  soup = BeautifulSoup(item_resp.text, "lxml")

  item_spec = soup.find(class_ = re.compile("item-spec"))
  subtitle       = item_spec.find(class_ = "subtitle").string
  title          = item_spec.find(class_ = "title").text + subtitle
  item_desc_list = item_spec.find(class_ = re.compile("desc-list")).text.strip("\r\n ").split("\n")
  suggest_price  = item_spec.find(class_ = "suggest").text.strip("\r\n ")
  special_price  = "特價" + item_spec.find(class_ = "priceinfo").text.strip("\r\n ")


def main():
  get_yahoo_item('123')


main()
