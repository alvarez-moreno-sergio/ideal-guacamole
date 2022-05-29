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

	def validate_secrets(dark):
		if dark['api_key'] == 'Your API KEY here' or dark['api_secret'] == 'Your SECRET key here':
			raise Exception('secrets.ini has not been set up. Please read https://github.com/alvarez-moreno-sergio/ideal-guacamole/tree/main#configuration')

	def load_secrets(path):
		dark_file = open(path, 'r')
		dark = json.loads(dark_file.read())

		Secrets.validate_secrets(dark)
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

import datetime
class Token:
	def __init__(self, symbol, pair, price, spot_quantity=0, earn_quantity=0):
		self._symbol = symbol
		self._pair = pair
		self._price = float(price)
		self._spot_quantity = spot_quantity
		self._earn_quantity = earn_quantity
		self._balance = 0
		self._timestamp = 0

	def symbol(self):
		return self._symbol

	def price(self):
		return self._price

	def spot_quantity(self):
		return self._spot_quantity

	def earn_quantity(self):
		return self._earn_quantity

	def pair(self):
		return self._pair

	def timestamp(self):
		return self._timestamp

	def get_price(self):
		market_data = BinanceAPI.market_price(self)

		if 'price' in market_data:
			self._price = float(market_data['price'])
		else:
			self._price = float(0)

		self.update_timestamp()
		return self._price

	def global_balance(self):
		return float(self._price) * (float(self.spot_quantity()) + float(self.earn_quantity()))

	def spot_balance(self):
		return float(self._price) * float(self.spot_quantity())

	def earn_balance(self):
		return float(self._price) * float(self.earn_quantity())

	def set_symbol(self, new):
		self._symbol = new

	def set_price(self, new):
		self._price = new

	def set_balance(self):
		self._balance = self.global_balance()

	def set_spot_quantity(self, new):
		self._spot_quantity = new

	def set_earn_quantity(self, new):
		self._earn_quantity = new

	def add_spot_quantity(self, new):
		self.set_spot_quantity(float(self.spot_quantity()) + float(new))

	def add_earn_quantity(self, new):
		self.set_earn_quantity(float(self.earn_quantity()) + float(new))

	def set_pair(self, new):
		self._pair = new

	def update_timestamp(self):
		self._timestamp = datetime.datetime.now()

	def update_token(self):
		self.get_price()
		self.set_balance()

		return self
		
	def __str__(self):
		result = "{"
		result += "\"symbol\": \"{}\",".format(self.symbol())
		result += " \"pair\": \"{}\",".format(self.pair())
		result += " \"price\": {},".format(self.price())
		result += " \"spot_quantity\": {},".format(self.spot_quantity())
		result += " \"earn_quantity\": {},".format(self.earn_quantity())
		result += " \"balance\": {},".format(self.global_balance())
		result += " \"timestamp\": \"{}\"".format(self.timestamp())
		result += "}"
		return result

	def to_hash(self):
		return json.loads(self.__str__())

	def cast(obj):
		result = Token(obj['symbol'], obj['pair'], obj['price'], obj['spot_quantity'], obj['earn_quantity'])
		result.update_token()
		return result

import os
from orm import Mongo
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
		# TokenManager.deserialize()
		Mongo.init()

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
	#       "_price":28752.78,
	#       "_spot_quantity":0.000000001,
	#       "_earn_quantity":0.000000001,
	#       "_balance":0.00002875278
	#    },
	#    "ETH":{
	#       "_symbol":"ETH",
	#       "_pair":"BUSD",
	#       "_price":1763.12,
	#       "_spot_quantity":0.000000001,
	#       "_earn_quantity":0.000000001,
	#       "_balance":0.00000176312
	#    }
	# }

	_tokens = {}

	def tokens():
		return TokenManager._tokens

	def add(token):
		TokenManager._tokens[token.symbol()] = token

	def size():
		return len(TokenManager._tokens)

	def serialize_to_file(content=None):
		if content == None: content = TokenManager.tokens()

		with open(Settings.tokens_path(), 'w') as output:
			content = TokenManager.serialize(content)
			output.write(content)

	def serialize(content):
		return json.dumps(content, default=lambda x: x.__dict__)

	def deserialize():
		load = None
		with open(Settings.tokens_path(), 'r') as file:
			lines = file.readline()
			if len(lines) > 0: load = json.loads(lines)
			
		if not load == None:
			for e in load:
				token = Token(load[e]['_symbol'], load[e]['_pair'], load[e]['_price'], load[e]['_spot_quantity'], load[e]['_earn_quantity'])
				TokenManager.add(token)
				# print(token)

		return TokenManager._tokens

