import datetime
import json

from edge_cases import SpecialTokens
from helpers import UI

from helpers import BinanceAPI
from lib import Binance
from lib import Secrets
from lib import Settings
from lib import Token
from lib import TokenManager
from orm import Mongo

# Debug
from helpers_test import Mock

tokens = {}
token_collection = None
start_date = datetime.date(2021, 11, 1)

def init():
	global token_collection

	Settings.initialize_env()
	mongo_db = Mongo.client().testing
	token_collection = mongo_db.tokens

def save_token(t, quantity, wallet):
	token = None
	if t.symbol() in tokens:
		token = tokens[t.symbol()]
	else:
		token = t

	if wallet == 'spot': token.add_spot_quantity(quantity)
	else: token.add_earn_quantity(quantity)

	token.update_token()
	tokens[token.symbol()] = token

	print("Updated {} data for symbol: {}".format(wallet, token.symbol()))
	TokenManager.add(token)

def calculate_payment_history():
	card_payment_history = BinanceAPI.get_fiat_payments_history_until_today_from(start_date)

	for e in card_payment_history:
		if e['cryptoCurrency'] == 'BUSD': continue
		
		tokens[e['cryptoCurrency']].add_invested_quantity(e['sourceAmount'])
		tokens[e['cryptoCurrency']].add_buy_price(e['price'])

def discover():
	global tokens

	# Switch comments to use Mock response
	# spot = Mock.get_spot_account_information()
	spot = BinanceAPI.get_spot_account_information()

	for e in spot['balances']:
		quantity = float(e['free']) + float(e['locked'])
		if quantity == 0: continue

		t = Token(e['asset'], 'BUSD', 0)
		if t.symbol()[:2] == 'LD':
			# earn asset
			t.set_symbol(t.symbol()[2:])
			save_token(t, quantity, 'earn')
		else:
			# spot asset
			save_token(t, quantity, 'spot')
			
	tokens = SpecialTokens.fix_tokens(tokens)
	calculate_payment_history()


init()
discover()
# Mongo.save_dict(token_collection, tokens)
UI.print_information(tokens)
