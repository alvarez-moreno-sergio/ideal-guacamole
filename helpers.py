import requests
import time
import json
import hmac
import hashlib

class BinanceAPI(object):

	__instance = None

	def __new__(cls):
		if BinanceAPI.__instance is None:
			BinanceAPI.__instance = object.__new__(cls)
		return BinanceAPI.__instance

	def set_uri(self, uri):
		self._uri = uri

	def set_api_key(self, key):
		self._key = key

	def set_api_secret(self, secret):
		self._secret = secret

	def uri(self):
		return self._uri

	def api_key(self):
		return self._key

	def api_secret(self):
		return self._secret

	def generate_signature(query_string):
		m = hmac.new(BinanceAPI().api_secret().encode("utf-8"), 
			query_string.encode("utf-8"), 
			hashlib.sha256)
		return m.hexdigest()

	def get_timestamp_offset():
	    url = "{}/api/v3/time".format(BinanceAPI().uri())
	    payload = {}
	    headers = {"Content-Type": "application/json"}
	    response = requests.request("GET", url, headers=headers, data=payload)
	    result = json.loads(response.text)["serverTime"] - int(time.time() * 1000)

	    return result

	def headers():
		return {"Content-Type": "application/json", "X-MBX-APIKEY": BinanceAPI().api_key()}

	def timestamp():
		return int(time.time() * 1000 + BinanceAPI.get_timestamp_offset())

	def market_price(token):
		api = BinanceAPI()
		query_string = "api/v3/ticker/price?symbol={}{}".format(token.symbol(), token.pair())
		url = "{}/{}".format(BinanceAPI().uri(), query_string)
		res = requests.get(url)
		data = res.json()

		# {'symbol': 'BTCBUSD', 'price': '29176.84000000'}
		return data


	def get_flexible_savings_balance(asset):
	    """ Get your balance in Bincance Earn :: Flexible Savings """
	    timestamp = BinanceAPI.timestamp()
	    query_string = "asset={}&timestamp={}".format(asset, timestamp)
	    signature = BinanceAPI.generate_signature(query_string)

	    url = "{}/sapi/v1/lending/daily/token/position?{}&signature={}".format(
	           BinanceAPI().uri(), query_string, signature)

	    payload = {}
	    headers = BinanceAPI.headers()

	    result = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

	    return result

	def get_all_earn_products():
	    """ Gets all savings products from Binance """
	    def get_earn_products(current_page=1):
	        """ Gets 50 savings products in "current" page ...modified from source:
	            https://binance-docs.github.io/apidocs/spot/en/#savings-endpoints """
	        timestamp = BinanceAPI.timestamp()
	        query_string = "&current={}&status=SUBSCRIBABLE&timestamp={}".format(
	                        current_page, timestamp)
	        signature = BinanceAPI.generate_signature(query_string)

	        url = "{}/sapi/v1/lending/daily/product/list?{}&signature={}".format(
	                  BinanceAPI().uri(), query_string, signature)

	        payload = {}
	        headers = BinanceAPI.headers()

	        result = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

	        return result
	    
	    all_products = []
	    more_products = True
	    current_page = 0

	    while more_products:
	        current_page += 1
	        prod = get_earn_products(current_page=current_page)
	        all_products.extend(prod)
	        if len(prod)==50:
	            more_products = True
	        else:
	            more_products = False

	    return all_products

	def get_spot_account_information():
		query_string = "timestamp={}".format(BinanceAPI.timestamp())
		url = "{}/api/v3/account?{}&signature={}".format(BinanceAPI().uri(), query_string, BinanceAPI.generate_signature(query_string))

		payload = {}
		headers = BinanceAPI.headers()

		res = requests.request("GET", url, headers=headers, data=payload).text
		result = json.loads(res)

		# [{'asset': 'LTC', 'free': '0.00000000', 'locked': '0.00000000'}, {'asset': 'ETH', 'free': '0.00000000', 'locked': '0.00000000'}, {'asset': 'NEO', 'free': '0.00000000', 'locked': '0.00000000'}]
		return result

from financial import Utils
class UI:
	def assets_to_print(assets):
		result = ''
		for e in assets: result += "\n" + assets[e].__str__()

		return result

	def print_information(tokens):
		print("==============")
		print("Here is your updated data: {}".format(UI.assets_to_print(tokens)))
		print("==============")

		balances = Utils.calculate_balances(tokens)
		print("Spot balance: {} €".format(balances['spot']))
		print("Earn balance: {} €".format(balances['earn']))
		print("Global balance: {} €".format(balances['global']))
