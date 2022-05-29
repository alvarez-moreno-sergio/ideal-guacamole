class Mock:
	def get_all_earn_products():
		# BinanceAPI.get_all_earn_products()

		return [{"asset":"BTC"},{"asset":"ETH"},{"asset":"XMR"}]

	def get_spot_account_information():
		# BinanceAPI.get_spot_account_information()
		
		return {'balances': [{'asset': 'BTC', 'free': '0.00000013', 'locked': '0.00000000'}, {'asset': 'ETH', 'free': '0.00000013', 'locked': '0.00000000'}, {'asset': 'XMR', 'free': '0.00000013', 'locked': '0.00000000'}]}
		
