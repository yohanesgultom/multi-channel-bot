import unittest
import os
import datetime
from channel.telegram import jobs
from channel.telegram.models import db, TradingPortfolio
from unittest import mock

class TestTelegramJobs(unittest.TestCase):

    @mock.patch('utils.indodax.requests')
    @mock.patch('channel.telegram.jobs.api_post')
    def test_send_indodax_summary(self, api_post, requests):
        user_id = 'user01'
        chat_id = 'user01'
        exchange = 'indodax'
        price_ref = 29000.0
        tickers = {
            'ada_idr': {
                'name': 'Cardano',
                'last': 30000,
                'server_time': '1628758964',
            }
        }        

        # mock requests
        response = mock.Mock()        
        response.json.return_value = {
            'tickers': tickers
        }
        requests.get = mock.Mock(return_value=response)

        # mock api
        api_post.return_value = {}

        # init db
        pair_name = next(iter(tickers))
        pair_data = tickers[pair_name]
        portfolio = TradingPortfolio(user_id=user_id, chat_id=chat_id, data={exchange: {pair_name: pair_data['last']}})
        db.session.add(portfolio)
        db.session.commit()

        # test
        jobs.send_indodax_summary()
        self.assertEqual(
            api_post.call_args_list[0],
            mock.call('sendMessage', data={'chat_id': chat_id, 'text': '💲 <b>Indodax Summary</b>\n\n🟢 <b>Cardano</b>: IDR 30,000 (0.0%)\n\n⏰️ 2021-08-12 16:02:44', 'parse_mode': 'HTML'})
        )
        self.assertTrue(True)

