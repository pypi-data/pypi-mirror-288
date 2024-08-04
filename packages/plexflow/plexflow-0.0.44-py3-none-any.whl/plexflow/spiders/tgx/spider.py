import scrapy
from bs4 import BeautifulSoup
from uuid import uuid4
from scrapy.exceptions import CloseSpider

class TgxSpider(scrapy.Spider): 
    name = "tgx_spider"
    session_expired: bool = False
    
    def __init__(self, host='https://torrentgalaxy.to', pages=None, start_page=None, num_pages=None, tag: str = str(uuid4()), dump_folder: str='.', cookies: dict = None):
        if pages is not None:
            self.pages = pages
        elif start_page is not None and num_pages is not None:
            self.pages = range(start_page, start_page + num_pages)
        else:
            raise ValueError("Either 'pages' or 'start_page' and 'num_pages' must be provided.")
        self.host = host
        self.tag = tag
        self.dump_folder = dump_folder
        self.cookies = cookies or {}
    
    def start_requests(self):
        for page_id in self.pages:
            yield scrapy.Request(
                f'{self.host}/torrent/{page_id}', 
                self.parse, 
                meta={'id': page_id},
                cookies=self.cookies)
    
    def parse(self, response):
        if self.session_expired:
            raise CloseSpider("Session Expired")
        soup = BeautifulSoup(response.text, 'html.parser')
        page_number = response.meta["id"]
        
        return {"soup": soup, "valid": True, "response": response, "meta": {"id": page_number}}
