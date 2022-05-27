import time
from lib import Secrets
from lib import Binance
from lib import Token
from helpers import BinanceAPI

# Debug
from test_helper import Mock

holding_tokens = []
holding_assets = []

tokens = {}

def assets_for_print(assets):
	result = ''
	for e in assets: result += "\n" + assets[e].__str__()

	return result

def fix_BUSD_tokens():
	# {"symbol": "BUSD","pair": "BUSD","price": "0.0","spot_quantity": "0.00370745","earn_quantity": "0","balance": "0.0"}
	token = tokens['BUSD']
	
	# calculates market price for EUR/BUSD
	aux_token = Token('EUR', 'BUSD', 0)
	eur_busd_price = BinanceAPI.market_price(aux_token)['price']

	# sets this market price to BUSD tokens
	# now BUSD tokens have EUR conversion price
	token.set_price(float(eur_busd_price))
	tokens['BUSD'] = token

def fix_BETH_tokens():
	# {"symbol": "BETH","pair": "BUSD","price": "0.0","spot_quantity": "0.00965173","earn_quantity": "0","balance": "0.0"}
	token = tokens['BETH']

	# calculates market price for BETH/ETH
	aux_token = Token('BETH', 'ETH', 0)
	beth_eth_price = BinanceAPI.market_price(aux_token)['price']

	# calculates market price for ETH/BUSD
	aux_token.set_symbol('ETH')
	aux_token.set_pair('BUSD')
	eth_busd_price = BinanceAPI.market_price(aux_token)['price']

	# calculates virtual market price for BETH/BUSD
	beth_busd_price = float(beth_eth_price) * float(eth_busd_price)

	# set price as conversion rate
	token.set_price(beth_busd_price)
	tokens['BETH'] = token

def fix_tokens():
	fix_BETH_tokens()
	fix_BUSD_tokens()

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

def discover():
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
			
	fix_tokens()

def calculate_balances():
	spot_balance  = float(0)
	earn_balance  = float(0)
	global_balance = float(0)

	for e in tokens:
		spot_balance += tokens[e].spot_balance()
		earn_balance += tokens[e].earn_balance()
		global_balance += tokens[e].global_balance()

	return convert_balances_to_EUR([spot_balance, earn_balance, global_balance])

def convert_balance_to_EUR(balance):
	# tokens['BUSD'] have EUR conversion price
	return float(balance) / float(tokens['BUSD'].price())

def convert_balances_to_EUR(balances):
	result = []
	for e in balances: result.append(convert_balance_to_EUR(e))

	return result


Settings.initialize_env()
discover()
TokenManager.serialize_to_file(tokens)
print("==============")
print("Here is your updated data: {}".format(assets_for_print(tokens)))
print("==============")

balances = calculate_balances()

print("Spot balance: {} €".format(balances[0]))
print("Earn balance: {} €".format(balances[1]))
print("Global balance: {} €".format(balances[2]))

