from time import sleep
from datetime import timedelta, datetime

import requests
from bs4 import BeautifulSoup

from . import logger


class WebLoader(object):
    DEFAULT_HEADERS = requests.structures.CaseInsensitiveDict({ 
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x87_64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    })

    def __init__(self, host=None, time_gap=None, headers=None, decode=None):
        self.session = requests.Session()
        self.host = host
        self.decode = decode
        self.session.headers = headers or self.DEFAULT_HEADERS
        self.last_req = None
        self.time_gap = time_gap
        if isinstance(self.time_gap, (float, int)):
            self.time_gap = timedelta(seconds=int(self.time_gap))

    def __del__(self):
        if self.session:
            self.session.close()

    def get(self, url, soup=True, headers=None, params=None):
        if self.last_req and self.time_gap:
            next_req = self.last_req + self.time_gap
            secs = (next_req - datetime.now()).total_seconds()
            if secs > 0:
                sleep(secs)
        if headers:
            resp = self.session.get(url, headers=headers, params=params)
        else:
            resp = self.session.get(url, params=params)

        self.last_req = datetime.now()
        
        if resp.status_code != 200:
            msg = 'Failed to get {}. {}: {}'.format(url, resp.status_code, resp.text)
            logger.error(msg)
            raise Exception(msg)
            
        if soup and resp.status_code == 200:
            if self.decode:
                text = resp.content.decode(self.decode)
            else:
                text = resp.text
            return BeautifulSoup(text, 'lxml')
        else:
            return resp
        