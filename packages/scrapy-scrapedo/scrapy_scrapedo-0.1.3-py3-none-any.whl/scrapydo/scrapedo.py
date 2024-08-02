
import urllib.parse
import json


class RequestParameters:
    def __init__(self,token:str,url:str|None=None, params:dict=None) -> None:
        self.apiurl = "https://api.scrape.do/"
        self.token = token
        self.url = url
        self.params = {k.lower(): v for k, v in params.items()} if params else {}
        assert self.token is not None and self.token != "", 'Scrape.do token is required'
        


    def encode(self) -> str:
        if "playwithbrowser" in self.params and isinstance(self.params["playwithbrowser"],list):
            self.params["playwithbrowser"] = json.dumps(self.params["playwithbrowser"],indent="")
        
        if "url" not in self.params:
            # that means if params has url, it will use that one.
            self.params["url"] = self.url
        
        encoded_params = '&'.join(f'{urllib.parse.quote(str(k))}={urllib.parse.quote(str(v),safe="")}' for k, v in self.params.items())
        return f'{self.apiurl}?token={self.token}&{encoded_params}'

    def copy(self) -> 'RequestParameters':
        return RequestParameters(
            token=self.token,
            url=self.url,
            params=self.params.copy()
        )


if __name__ == "__main__":
    # small unit test
    print(RequestParameters(
        url="https://httpbin.co/",
        token="TOKEN",
        params={
            "render":True,
            "geoCode":"us",
            "playWithBrowser":[
                {
                    "Action": "Click",
                    "Selector":"#manpage > div.mp > ul > li:nth-child(3) > a"
                },
                {
                    "Action":"Wait",
                    "Timeout":2000,
                },{
                    "Action":"Execute",
                    "Execute":"document.URL",
                }
            ],
        },
    ).encode())

        

