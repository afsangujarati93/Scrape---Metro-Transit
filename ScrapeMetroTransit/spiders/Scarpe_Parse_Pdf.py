# -*- coding: utf-8 -*-
#from PyPDF2 import PdfFileReader #not efficient for my purpose
#pdfminer not efficient for my purpose
from tabula import read_pdf
from Log_Handler import Log_Handler as lh

logger = lh.log_initializer()

class ParseResponse:
    
    def parse_pdf():
        try:
            df = read_pdf("Route01.pdf")

            df = df.drop(df.index[0])
            df = df.dropna(axis=1, how= "all")
            df = df.dropna(axis=0, how= "all")
            df = df.iloc[3:]
            df.to_csv("output_csv.csv", encoding='utf-8')
        except Exception as Ex:
#            print("Exception occurred in the QuotesSpider method| Exception:" + str(Ex))
            logger.error("Exception occurred in the start_requests method| Exception:" + str(Ex))          
   
            


