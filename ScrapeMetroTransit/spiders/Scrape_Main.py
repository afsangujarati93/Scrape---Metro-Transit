# -*- coding: utf-8 -*-
#about yield https://www.pythoncentral.io/python-generators-and-yield-keyword/
import scrapy
from Log_Handler import Log_Handler as lh
from scrapy.http import Request
import os
logger = lh.log_initializer()

class MetroSpider(scrapy.Spider):
    name = "metrotransit"
    def start_requests(self):
        try:
            urls = [
                'https://www.halifax.ca/transportation/halifax-transit/routes-schedules',            
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.scrape_schedules)
        except Exception as Ex:
            logger.error("Exception occurred in the start_requests method| Exception:" + str(Ex))          
                
    def save_pdf(self, response):
        try: 
            path = response.url.split('/')[-1]                     
            logger.info('Saving PDF %s', path)
            with open(path, 'wb') as f:
                f.write(response.body)            
        except Exception as Ex:
            logger.error("Exception occurred in the save_pdf method| Exception:" + str(Ex))          
   
            
    def scrape_schedules(self, response):
        try:
            #The number of . in the path signifies how many steps you want to go back
            #here it is one . so it will go one step back the spiders direc(which is the current direc)
            #and search for folder Route Schedules and than create the file in it
            #and chdir => change directory
            os.chdir("./Route Schedules")
            metrotr = response.css(".c-table__body tr")
            for metro in metrotr:
                metro = metro.css("td")[2]
                metro = metro.css("a::attr(href)").extract_first()
                yield{                  
                        'text_test' : metro
                     }
                yield Request(
                        url=response.urljoin(metro),    
                        callback=self.save_pdf
                     ) 
#          for metrotr in response.css(".c-table__body tr"):
#              i = 0
#              text_tag = ''
#              for metrotd in metrotr.css("td"):                  
#                  if i ==0:
#                      text_tag = "route_num"
#                  elif i== 1:
#                      text_tag = "route_description"
#                  elif i ==2: 
#                      text_tag = "route_schedule"
#                      metro = metro.css("a::attr(href)").extract_first()
#                      yield Request(
#                                url=response.urljoin(metro),    
#                                callback=self.save_pdf
#                            )
#                  elif i ==3: 
#                      text_tag = "route_map"
#                  yield{                  
#                          text_tag : metrotd.css("::text").extract_first()
#                        }
#                  i+=1
        except Exception as Ex:
            logger.error("Exception occurred in the parse method| Exception:" + str(Ex))
                
        