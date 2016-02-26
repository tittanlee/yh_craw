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
      get_yahoo_category(sub_title_url)

def get_yahoo_category(yahoo_cate_url):
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
        # print("%s %s" %(stitle, stitle_url))
      except:
        # print("%s" %(stitle))
        break

    for cate_list in site_list.select(".list"):
      print(cate_list)
      # cate_name = cate_list.a.get_text()
      # cate_url  = YAHOO_BASE_URL + cate_list.a.get('href')
      # print(cate_name)
      # print(cate_url)
      # get_yahoo_item(cate_url)

def has_class_but_id_null(tag):
  return tag['class'] == ".list" #and tag['id'] != ""

def get_yahoo_item(yahoo_cate_item_url):

  #
  # Get recommend products
  #
  yahoo_resp = requests.get(yahoo_cate_item_url )
  yahoo_resp.encoding = "utf-8"
  soup = BeautifulSoup(yahoo_resp.text, "lxml")
  recommend_item = soup.find("div", attrs = {'id' : 'cl-recproduct'})

  for rec_item in recommend_item.select(".name"):
    rec_item_name = rec_item.string
    rec_item_link = rec_item.a.get('href')
    get_detail_item_info(rec_item_link)

  #
  # get group products
  # 
  page_dict = get_paging_dict(yahoo_cate_item_url)
  for page, link in page_dict['paging'].items():
    yahoo_resp = requests.get(link)
    yahoo_resp.encoding = "utf-8"
    soup = BeautifulSoup(yahoo_resp.text, "lxml")
    group_product = soup.find("div", attrs = {'id' : 'cl-gproduct'})
    for item in group_product.select(".name"):
      item_name = item.string
      item_link = item.a.get('href')
      get_detail_item_info(item_link)

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
  item_spec = soup.find(class_ = "item-spec")

  subtitle       = item_spec.select(".subtitle")
  if(len(subtitle)):
    subtitle     = subtitle[0].get_text()
  else:
    subtitle     = ""

  title          = item_spec.select(".title")[0].get_text()
  item_desc      = item_spec.select(".desc-list")[0].get_text().strip()
  suggest_price  = item_spec.select(".suggest")[0].get_text()
  special_price  = "特價" + item_spec.select(".priceinfo")[0].get_text().strip()


  print(yahoo_item_url)
  print(subtitle)
  print(title)
  print(item_desc)
  print(suggest_price)
  print(special_price)

  print("\n")



def main():
  get_yahoo_title()

main()
