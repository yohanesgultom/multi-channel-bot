import unittest
import datetime
import os
from unittest import mock
from channel.telegram import commands
from channel.telegram.models import db, TradingPortfolio

class TestTradingPortfolio(unittest.TestCase):

    def setUp(self):
        db.session.query(TradingPortfolio).delete()
        db.session.commit()

    @mock.patch('utils.indodax.requests')
    def test_add_get(self, requests):
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
        response = mock.Mock()        
        response.json.return_value = {
            'tickers': tickers
        }
        requests.get = mock.Mock(return_value=response)

        # before adding
        reply = commands.indodax(user_id)
        self.assertEqual(reply, {'text': 'ℹ️ No portfolio found', 'parse_mode': 'html'})

        # add
        reply = commands.trading_portfolio_add(user_id, chat_id, exchange, next(iter(tickers)), price_ref)
        self.assertEqual(reply, {'text': '✅ Portfolio updated', 'parse_mode': 'html'})
        
        # after adding
        reply = commands.indodax(user_id)
        self.assertEqual(reply, {'text': '💲 <b>Indodax Summary</b>\n\n🟢 <b>Cardano</b>: IDR 30,000 (3.4%)\n\n⏰️ 2021-08-12 16:02:44', 'parse_mode': 'html'})

    @mock.patch('utils.indodax.requests')
    def test_update_get(self, requests):
        user_id = 'user01'
        chat_id = 'user01'
        exchange = 'indodax'
        price_ref = 29000.0
        tickers = {
            'ada_idr': {
                'name': 'Cardano',
                'last': 30000,
                'server_time': '1628758964',
            },
            'dot_idr': {
                'name': 'Polkadot',
                'last': 301000,
                'server_time': '1628758964',
            },
        }
        response = mock.Mock()        
        response.json.return_value = {
            'tickers': tickers
        }
        requests.get = mock.Mock(return_value=response)

        # before updating
        reply = commands.trading_portfolio_add(user_id, chat_id, exchange, next(iter(tickers)), price_ref)
        reply = commands.indodax(user_id)
        self.assertEqual(reply, {'text': '💲 <b>Indodax Summary</b>\n\n🟢 <b>Cardano</b>: IDR 30,000 (3.4%)\n\n⏰️ 2021-08-12 16:02:44', 'parse_mode': 'html'})

        # update
        update_pair_name = list(tickers.keys())[1]
        update_pair_data = tickers[update_pair_name]
        update_price_ref = 299000
        reply = commands.trading_portfolio_add(user_id, chat_id, exchange, update_pair_name, update_price_ref)
        self.assertEqual(reply, {'text': '✅ Portfolio updated', 'parse_mode': 'html'})
        
        # after adding
        reply = commands.indodax(user_id)
        self.assertEqual(reply, {'text': '💲 <b>Indodax Summary</b>\n\n🟢 <b>Cardano</b>: IDR 30,000 (3.4%)\n🟢 <b>Polkadot</b>: IDR 301,000 (0.7%)\n\n⏰️ 2021-08-12 16:02:44', 'parse_mode': 'html'})        

    @mock.patch('utils.indodax.requests')
    def test_del_get(self, requests):
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
        response = mock.Mock()        
        response.json.return_value = {
            'tickers': tickers
        }
        requests.get = mock.Mock(return_value=response)

        # before deleting
        reply = commands.trading_portfolio_add(user_id, chat_id, exchange, next(iter(tickers)), price_ref)        
        reply = commands.indodax(user_id)
        self.assertEqual(reply, {'text': '💲 <b>Indodax Summary</b>\n\n🟢 <b>Cardano</b>: IDR 30,000 (3.4%)\n\n⏰️ 2021-08-12 16:02:44', 'parse_mode': 'html'})

        # delete
        reply = commands.trading_portfolio_del(user_id, chat_id, exchange, next(iter(tickers)))
        self.assertEqual(reply, {'text': '✅ Pair removed', 'parse_mode': 'html'})

        # after deleting
        reply = commands.indodax(user_id)
        self.assertEqual(reply, {'text': 'ℹ️ No portfolio found', 'parse_mode': 'html'})



