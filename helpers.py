import requests
from datetime import date
from datetime import datetime
import dateutil.relativedelta as relativedelta
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

	def get_timestamp_milliseconds_since_epoch(startTime):
		# startTime = '01/01/2019'
		return round(datetime.strptime(startTime, "%Y-%m-%d").timestamp()*1000)

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

	def get_trades_for_symbol(token):
		query_string = "symbol={}&timestamp={}".format(token.trade_pairs(), BinanceAPI.timestamp())
		url = "{}/api/v3/myTrades?{}&signature={}".format(BinanceAPI().uri(), query_string, BinanceAPI.generate_signature(query_string))

		payload = {}
		headers = BinanceAPI.headers()

		res = requests.request("GET", url, headers=headers, data=payload).text
		result = json.loads(res)

		# [{"symbol":"BTCBUSD","id":1,"orderId":1,"orderListId":-1,"price":"47655.50000000","qty":"0.1","quoteQty":"10.1","commission":"0.00001","commissionAsset":"BTC","time":1,"isBuyer":true,"isMaker":false,"isBestMatch":true},{"symbol":"BTCBUSD","id":2,"orderId":2,"orderListId":-1,"price":"47655.10000000","qty":"0.1","quoteQty":"10.1","commission":"0.00001","commissionAsset":"BTC","time":2,"isBuyer":true,"isMaker":false,"isBestMatch":true}]
		return result

	def get_fiat_payments_history(beginTime=0, endTime=0):
		transaction_type = 0 # 'buy'

		query_string = "transactionType={}&timestamp={}".format(transaction_type, BinanceAPI.timestamp())
		if beginTime != 0: query_string+= "&beginTime={}".format(BinanceAPI.get_timestamp_milliseconds_since_epoch(beginTime))
		if endTime != 0: query_string+= "&endTime={}".format(BinanceAPI.get_timestamp_milliseconds_since_epoch(endTime))
		url = "{}/sapi/v1/fiat/payments?{}&signature={}".format(BinanceAPI().uri(), query_string, BinanceAPI.generate_signature(query_string))

		payload = {}
		headers = BinanceAPI.headers()

		res = requests.request("GET", url, headers=headers, data=payload).text
		result = json.loads(res)

		# {"code":"000000","message":"success","data":[{"orderNo":"e8c75bde2dfb423f8cec3d5774414e35","sourceAmount":"200.0","fiatCurrency":"EUR","obtainAmount":"217.28869402","cryptoCurrency":"BUSD","totalFee":"4.0","price":"0.90202576","status":"Completed","createTime":1640731933000,"updateTime":1640731963000},{"orderNo":"N01168006920136168448121606","sourceAmount":"50.0","fiatCurrency":"EUR","obtainAmount":"54.30072801","cryptoCurrency":"BUSD","totalFee":"1.00","price":"0.90238201","status":"Completed","createTime":1639669720000,"updateTime":1639669757666}]}
		return result		

	def get_fiat_payments_history_until_today_from(beginDate, months_interval=3):
		result = []
		today = date.today()
		endDate = today - relativedelta.relativedelta(days=1)
		while(today >= endDate):
			endDate = beginDate + relativedelta.relativedelta(months=months_interval)
			api_res = BinanceAPI.get_fiat_payments_history(beginDate.__str__(), endDate.__str__())
			beginDate = endDate

			if 'data' in api_res.keys():
				for e in api_res['data']: 
						if e['status'] == 'Completed': 
							result.append(e)

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
