#!/usr/bin/env python

from datetime import datetime

from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer, SimpleProducer

import settings
import sys

from cassandra.cluster import Cluster

cluster = Cluster(['IPADDRESS'])
session = cluster.connect('KEY')
session.default_timeout = 30 # 30 seconds

# sort male and female shoes if data exists
def get_category(match, category=" "):
  if match == "95672":
      category = "F"
  elif match in ["15709","24087"]:
      category = "M"
  else:
      category ="u"
  return category

# simple categorizing
def get_shoe(match, shoe=" "):
  if "yeezy" in match:
      shoe = "YEEZY"
  if "jordan" in match:
      shoe = "JORDAN"
  if "flyknit" in match:
      shoe = "FLYKNIT"
  if "max" in match:
      shoe = "AIR_MAX"
  if "curr" in match:
      shoe = "CURRY"
  return shoe

# get existing list of ID's
def checkCassandra():
  stmt = "SELECT shoeid, starttime FROM justsoldonebay"
  response = session.execute(stmt)
  ids = [x.shoeid for x in response]
  return ids  

class Producer(object):

    def __init__(self, addr):
        self.client = KafkaClient(addr)
        self.producer = KeyedProducer(self.client)

    def open_save(self, fileName):
        log_file = open(fileName, "w")
        log_file.close()
        return log_file

    def produce_msgs(self, source_symbol, topic, items):
      print datetime.now()

      sample = []
      saved = checkCassandra()

      for item in items:
          listing = []
          log_file = open("justsoldonebay.csv", "a")

          if item.sellingStatus.sellingState == "EndedWithSales":
              gender = get_category(item.primaryCategory.categoryId)
              shoe = get_shoe(item.title.lower())

              if item.itemId in saved: 
                print item.itemId, item.title
              if item.itemId not in saved:

                zip_code2 = ""
                try:
                    zip_code = item.postalCode
                    try:
                        int(zip_code)
                    except:
                        zip_code = 0
                        # save it elsewhere
                        zip_code2 = item.postalCode
                except: 
                    zip_code = 0

                try:
                    location = item.location
                except: 
                    location = "0"

                try:
                    gallery = item.galleryURL
                except:
                    gallery = "NA"

                
                price = item.sellingStatus.convertedCurrentPrice.value
                pprice = "${}{}".format(price,item.sellingStatus.convertedCurrentPrice._currencyId)        
                #print item.listingInfo.startTime, item.itemId, shoe, price, zip_code, gender #, item.title
                start = str(item.listingInfo.startTime)
                end = str(item.listingInfo.endTime)
                listing = [start, item.listingInfo.endTime, item.viewItemURL,
                           item.itemId, shoe, price, zip_code, gender, gallery, 
                           location, item.title, zip_code2]
                sample.append(listing)


      msg_cnt = 0
      while True:
        str_fmt = "{};{};{};{};{};{};{};{};{};{};{};{}"
        x = sample[msg_cnt]
        message_info = str_fmt.format(x[0], x[1], x[2],
                                      x[3], x[4], x[5],
                                      x[6], x[7], x[8],
                                      x[9], x[10], x[11])
        print message_info
        log_file.write(str(len(x)) +" "+message_info+ "\n")
        self.producer.send_messages('justsoldonebay', "1", message_info)
        msg_cnt += 1
        if msg_cnt == len(sample):
          break
        

#client = KafkaClient("ec2-54-173-157-255.compute-1.amazonaws.com")
#producer = SimpleProducer(client)

if __name__ == "__main__":
    ip_addr = "PUBLIC_DNS"  
    prod = Producer(ip_addr)
    #prod.open_save("justsoldonebay.csv")
    
    args = sys.argv
    if len(args) > 1:
      if args[1] == "airmax":
        kw = "(air%20max)"
      else:
        kw = args[1]
    else:
      kw = "(yeezy,jordan,air%20max,curry,flyknit)"
    
    # eBay Connection
    api = Connection(appid=settings.EBAY_APP, config_file=None)
    api_request = {
                  'keywords': kw,
                  'categoryId': ['15709', '24087', '95672'],
                  'sortOrder': 'StartTimeNewest',
              }
    response = api.execute('findCompletedItems', api_request)
    items = response.reply.searchResult.item

    prod.produce_msgs("1", "justsoldonebay", items)
