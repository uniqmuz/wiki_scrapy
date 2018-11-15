import logging
from scrapy.conf import settings

def parseHeader(response):
    logging.info("header : " + response.text)
    return None
    