import json
class Secrets:
	_api_key = None
	_api_secret = None

	def __init__(self, secrets):
		self._api_key = secrets['api_key']
		self._api_secret = secrets['api_secret']
		self._secrets = secrets

	def api_key(self):
		return self._api_key

	def api_secret(self):
		return self._api_secret

	def load_secrets(path):
		dark_file = open(path, 'r')
		dark = json.loads(dark_file.read())
		return Secrets(dark)


from helpers import BinanceAPI

class Binance:
	def __init__(self, secrets):
		self._secrets = secrets

	def api_uri(self):
		return self._secrets._secrets['binance_api_uri']

	def api_key(self):
		return self._secrets.api_key()


	def init_api(self):
		BinanceAPI().set_uri(self.api_uri())
		BinanceAPI().set_api_key(self.api_key())
		BinanceAPI().set_api_secret(self._secrets.api_secret())


class Token:
	def __init__(self, symbol, pair, price, wallet, holding_quantity=0):
		self._symbol = symbol
		self._pair = pair
		self._price = float(price)
		self._wallet = wallet
		self._holding_quantity = holding_quantity

	def symbol(self):
		return self._symbol

	def price(self):
		return self._price

	def holding_quantity(self):
		return self._holding_quantity

	def pair(self):
		return self._pair

	def wallet(self):
		return self._wallet

	def get_price(self):
		market_data = BinanceAPI.market_price(self)

		if 'price' in market_data:
			self._price = float(market_data['price'])
		else:
			self._price = float(0)

		return self._price

	def balance(self):
		return float(self._price) * float(self.holding_quantity())

	def set_symbol(self, new):
		_symbol = new

	def set_holding_quantity(self, new):
		_holding_quantity = new

	def set_pair(self, new):
		_pair = new

	def set_wallet(self, new):
		_wallet = new

	def update_token(self, new):
		self.get_price()
		self.set_wallet(new.wallet())
		self.set_holding_quantity(new.holding_quantity())

		return self
		
	def __str__(self):
		result = "{"
		result += "\"symbol\": \"{}\",".format(self.symbol())
		result += "\"pair\": \"{}\",".format(self.pair())
		result += "\"price\": \"{}\",".format(self.price())
		result += "\"holding_quantity\": \"{}\",".format(self.holding_quantity())
		result += "\"balance\": \"{}\",".format(self.balance())
		result += "\"wallet\": \"{}\"".format(self.wallet())
		result += "}"
		return result

import os
class Settings:
	_log_path = './'
	_log_name = 'log.log'
	_tokens_name = 'tokens.json'
	_secrets_name = 'secrets.ini'

	def initialize_env():
		Settings.check_log_files()
		secrets = Secrets.load_secrets(Settings.secrets_path())
		binance = Binance(secrets)
		binance.init_api()
		TokenManager.deserialize()

	def log_path():
		return Settings._log_path + Settings._log_name

	def tokens_path():
		return Settings._log_path + Settings._tokens_name

	def secrets_path():
		return Settings._log_path + Settings._secrets_name

	def create_if_missing(path):
		if not os.path.exists(path):
				open(path, 'w').close()	

	def check_log_files():
		Settings.create_if_missing(Settings.log_path())
		Settings.create_if_missing(Settings.tokens_path())

class TokenManager:
	# expected structure (dict):
	# {
	#    "BTC":{
	#       "_symbol":"BTC",
	#       "_pair":"BUSD",
	#       "_price":29476.92,
	#       "_wallet":"earn",
	#       "_holding_quantity":"0.000000001"
	#    },
	#    "ETH":{
	#       "_symbol":"ETH",
	#       "_pair":"BUSD",
	#       "_price":1829.75,
	#       "_wallet":"earn",
	#       "_holding_quantity":"0.000000001"
	#    },
	#    "XMR":{
	#       "_symbol":"XMR",
	#       "_pair":"BUSD",
	#       "_price":189.0,
	#       "_wallet":"earn",
	#       "_holding_quantity":"0.000000001"
	#    }
	# }

	_tokens = {}

	def tokens():
		return TokenManager._tokens

	def add(token):
		TokenManager._tokens[token.symbol()] = token

	def update(token):
		TokenManager.add(token)

	def size():
		return len(TokenManager._tokens)

	def toJson(tokens=[]):
		if len(tokens) == 0: tokens = TokenManager.tokens()

		result = "{"
		for e in tokens:
			result += "{} : ".format(e)
			result += "{"
			result += tokens[e].__str__()
			result += "}"

		result = result[:-1] + "]}"
		return result

	def serialize_to_file(content=None):
		if content == None: content = TokenManager.tokens()

		with open(Settings.tokens_path(), 'w') as output:
			content = json.dumps(content, default=lambda x: x.__dict__)
			output.write(content)

	def deserialize():
		load = None
		with open(Settings.tokens_path(), 'r') as file:
			lines = file.readline()
			if len(lines) > 0: load = json.loads(lines)
			
		if not load == None:
			for e in load:
				token = Token(load[e]['_symbol'], load[e]['_pair'], load[e]['_price'], load[e]['_wallet'], load[e]['_holding_quantity'])
				TokenManager.add(token)
		return TokenManager._tokens

