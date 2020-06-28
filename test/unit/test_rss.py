import unittest
import datetime
import os
from unittest import mock
from utils.rss import RSSParser

class TestRSS(unittest.TestCase):

    @mock.patch('utils.rss.requests')
    def test_fetch(self, requests):
        with open(os.path.join('test', 'files', 'example_rss_1.xml'), 'rb') as f:
            content = f.read()
        response = mock.Mock()        
        response.content = content
        requests.get = mock.Mock(return_value=response)
        p = RSSParser()
        results = p.fetch('https://www.upwork.com')
        self.assertEqual(len(results), 10)

    def test_parse_description_upwork(self):
        descriptions = [
            'customizing the pages of a learndash website using elumine theme.\n\n<b>Hourly Range</b>: $13.00-$25.00\n\n\n<b>Posted On</b>: June 24, 2020 08:24 UTC\n<b>Category</b>: CMS Customization\n<b>Skills</b>:LearnDash,     Website,     BuddyPress,     Plugins for Wordpress,     Elementor,     Website Customization    \n\n<b>Country</b>: Saudi Arabia\n\n<a href="https://www.upwork.com/jobs/learndash-elumine-website-completion_%7E015935afca83bb86a9?source=rss">click to apply</a>',
            'API integration developer with experience in PHP, Python, JavaScript for long term relationship with a one of a kind service\n\n<b>Hourly Range</b>: $17.00-$37.00\n\n\n<b>Posted On</b>: June 24, 2020 07:57 UTC\n<b>Category</b>: Scripting & Automation\n\n<b>Country</b>: Israel\n\n<a href="https://www.upwork.com/jobs/API-integration-developer-with-experience-PHP-Python-JavaScript_%7E013d9dbec749e4274f?source=rss">click to apply</a>',
            'we need an Odoo developer to implement some customize feature to our Oddo 12 community edition.\n\n\n<b>Posted On</b>: June 24, 2020 07:54 UTC\n<b>Category</b>: Full Stack Development\n<b>Skills</b>:Odoo    \n\n<b>Country</b>: United Arab Emirates\n\n<a href="https://www.upwork.com/jobs/Odoo-community-customization_%7E01f452252ea5c086ef?source=rss">click to apply</a>',           
        ]
        expected = [
            {'rate_low': 13.0, 'rate_high': 25.0, 'cat': 'CMS Customization', 'skills': ['LearnDash', 'Website', 'BuddyPress', 'Plugins for Wordpress', 'Elementor', 'Website Customization'], 'country': 'Saudi Arabia'},
            {'rate_low': 17.0, 'rate_high': 37.0, 'cat': 'Scripting & Automation', 'skills': None, 'country': 'Israel'},
            {'rate_low': None, 'rate_high': None, 'cat': 'Full Stack Development', 'skills': ['Odoo'], 'country': 'United Arab Emirates'},
        ]
        p = RSSParser()
        res = [p.parse_description_upwork(d) for d in descriptions]
        self.assertEqual(res, expected)


