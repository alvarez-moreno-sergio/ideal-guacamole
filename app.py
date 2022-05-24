import time
from lib import Secrets
from lib import Binance
from lib import Token
from helpers import BinanceAPI

# Debug
from test_helper import Mock

holding_tokens = []
holding_assets = []

end_discover_data = False

def save_token(asset):
	global end_discover_data
	token = Token(asset['asset'], 'BUSD', asset['totalAmount'])

	if not end_discover_data:
		holding_assets.append({"asset": asset['asset']})	
		holding_tokens.append(token)

	print(token)


def discover_data(assets=[]):
	global end_discover_data

	if len(assets) > 0: print(assets)
	if len(assets) == 0: assets = BinanceAPI.get_all_earn_products()
	
	# Uncomment to mock Binance response for a shorter debug version
	# assets = Mock.mock_get_all_earn_products() 

	for e in assets:
		asset = BinanceAPI.get_flexible_savings_balance(e['asset'])
		if len(asset) == 0: continue

		save_token(asset[0])
	end_discover_data = True

secrets = Secrets.load_secrets()
binance = Binance(secrets)
binance.init_api()


discover_data()
print(holding_tokens)
i = 0
while (True):
	i+=1
	print('======================================')
	time.sleep(1)
	discover_data(holding_assets)

print('======================================')
print(holding_tokens)
print(holding_assets)
