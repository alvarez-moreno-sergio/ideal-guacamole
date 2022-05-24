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

	def load_secrets():
		dark_file = open('./config.ini', 'r')
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
	def __init__(self, symbol, pair, holding_quantity=0):
		self._symbol = symbol
		self._pair = pair
		self._price = float(0.0)
		self._holding_quantity = holding_quantity

	def symbol(self):
		return self._symbol

	def price(self):
		return self._price

	def holding_quantity(self):
		return self._holding_quantity

	def pair(self):
		return self._pair

	def price(self):
		market_data = BinanceAPI.market_price(self)

		if 'price' in market_data:
			self._price = float(market_data['price'])
		else:
			self._price = float(0)

		return self._price

	def balance(self):
		return float(self._price) * float(self.holding_quantity())

	def __str__(self):
		price = self.price()

		result = "{"
		result += "\"symbol\": \"{}\",".format(self.symbol())
		result += "\"pair\": \"{}\",".format(self.pair())
		result += "\"price\": \"{}\",".format(price)
		result += "\"holding_quantity\": \"{}\",".format(self.holding_quantity())
		result += "\"balance\": \"{}\"".format(self.balance())
		result += "}"
		return result
