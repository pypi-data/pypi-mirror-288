from typing import Any
import scrapy
from scrapy import Request
from scrapy import *
from . import scrapedo
import urllib.parse

class Spider(scrapy.Spider):
    def __init__(self, params: scrapedo.RequestParameters ,*args: Any, **kwargs: Any):
        self.params = params
        super().__init__(*args, **kwargs)
        

    def Request(self,*args: Any, **kwargs: Any) -> Request:
        return Request(self.params,*args, **kwargs)
    
    def origin_url(self,url: str) -> str:
        res = urllib.parse.urlparse(url)
        return urllib.parse.parse_qs(res.query)["url"][0]
    
    def target_url(self,response) -> str:
        return response.headers["Scrape.do-Target-Url"]
    
        
    
    

class Request(scrapy.Request):
    def __init__(self, params: scrapedo.RequestParameters, *args: Any, **kwargs: Any):
        
        url = kwargs.get("url")
        assert url is not None, "url is required"

        p = params.copy()
        p.params["url"] = url
        kwargs["url"] = p.encode()
        print(kwargs)
        super().__init__(*args, **kwargs)