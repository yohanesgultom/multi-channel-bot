import requests
import logging
import os
from bs4 import BeautifulSoup
from datetime import datetime, timezone

class RSSParser:
    def fetch(self, url, last_update=None):
        headers = {'User-Agent':'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        content = res.content
        soup = BeautifulSoup(content, 'lxml-xml')
        items = soup.find_all('item')      

        # parse results
        results = []
        for item in items:
            record = {}
            for tag in item.children:
                if tag.name:
                    val = tag.string
                    if tag.name == 'pubDate':
                        val = datetime.strptime(val, '%a, %d %b %Y %H:%M:%S %z')
                    elif tag.name == 'encoded' or tag.name == 'description':
                        val = val.replace('<br />', '\n').replace('&nbsp;', '').strip()
                    record[tag.name] = val        
            # include if no last_update
            # or pubDate is newer than last_update
            if not last_update \
                or ('pubDate' in record and record['pubDate'] > last_update):
                results.append(record)
        return results
