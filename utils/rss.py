import requests
import logging
import os
import re
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
                        val = val \
                            .replace('<br />', '\n') \
                            .replace('&nbsp;', '') \
                            .replace('&quot;', '"') \
                            .replace('&gt;', '>') \
                            .replace('&lt;', '<') \
                            .replace('&amp;', '&') \
                            .strip()
                    record[tag.name] = val        
            # extract more info
            if url.startswith('https://www.upwork.com'):
                details = self.parse_description_upwork(record['description'])
                record.update(details)
            # include if no last_update
            # or pubDate is newer than last_update
            if not last_update \
                or ('pubDate' in record and record['pubDate'] > last_update):
                results.append(record)
        return results

    def parse_description_upwork(self, description):
        """
        <b>Hourly Range</b>: $13.00-$25.00\n\n\n<b>Posted On</b>: June 24, 2020 08:24 UTC\n<b>Category</b>: CMS Customization\n<b>Skills</b>:LearnDash,     Website,     BuddyPress,     Plugins for Wordpress,     Elementor,     Website Customization    \n\n<b>Country</b>: Saudi Arabia\n\n
        """            
        rate_low = None
        rate_high = None
        cat = None
        skills = None
        country = None
        
        rate_pattern = re.compile("<b>Hourly Range<\/b>: \$(\d+\.\d+)-\$(\d+\.\d+)\n")
        match = rate_pattern.search(description)
        if match:
            rate_low = float(match[1])
            rate_high = float(match[2])

        cat_pattern = re.compile("<b>Category<\/b>: ([^\n]+)\n")
        match = cat_pattern.search(description)
        if match:
            cat = match[1].strip()

        skills_pattern = re.compile("<b>Skills<\/b>:([^\n]+)\n")
        match = skills_pattern.search(description)
        if match:
            skills = [s.strip() for s in match[1].split(',')]

        country_pattern = re.compile("<b>Country<\/b>: ([^\n]+)\n")
        match = country_pattern.search(description)
        if match:
            country = match[1].strip()

        return {
            'rate_low': rate_low,
            'rate_high': rate_high,
            'cat': cat,
            'skills': skills,
            'country': country,
        }