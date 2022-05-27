import json
from lib import Settings
from lib import Secrets
from lib import Binance
from lib import Token
from lib import TokenManager
from helpers import BinanceAPI

# Debug
from helpers_test import Mock

tokens = {}
end_discover_data = False

def print_assets(assets):
	for e in assets:
		print(assets[e])

def update_flexible_token(asset):
	token = tokens[asset.symbol()]
	updated_token = token.update_token(asset)
	tokens[asset.symbol()] = updated_token

def save_flexible_token(asset):
	token = Token(asset['asset'], 'BUSD', 0, 'earn', asset['totalAmount'])
	token.get_price()
	tokens[asset['asset']] = token

def discover_data(assets=[]):
	assets = {}
	if TokenManager.size() == 0:
		assets = TokenManager.deserialize()
	else:
		assets = TokenManager.tokens()
	
	print_assets(assets)

	# Switch comments to mock Binance response for a shorter debug version
	if len(assets) == 0: assets = BinanceAPI.get_all_earn_products()
	# if len(assets) == 0: assets = Mock.get_all_earn_products()

	for e in assets:
		payload = None
		if TokenManager.size() > 0:
			payload = e
		else:
			payload = e['asset']

		asset = BinanceAPI.get_flexible_savings_balance(payload)
		if len(asset) == 0: continue

		if isinstance(asset, Token):
			update_flexible_token(asset[0])
		else:
			save_flexible_token(asset[0])

# ============ MAIN ============

Settings.initialize_env()
discover_data()
TokenManager.serialize_to_file(tokens)
print_assets(tokens)
