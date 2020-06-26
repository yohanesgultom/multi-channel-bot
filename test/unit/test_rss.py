import unittest
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
        results = p.fetch(None)
        print(results)
        self.assertEqual(len(results), 10)
