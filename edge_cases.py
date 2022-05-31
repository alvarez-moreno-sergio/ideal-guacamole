from lib import Token
from lib import TokenManager
from helpers import BinanceAPI
class SpecialTokens:
	def fix_BUSD_tokens(busd_token):
		# {"symbol": "BUSD","pair": "BUSD","price": "0.0","spot_quantity": "0.00370745","earn_quantity": "0","balance": "0.0"}
		
		# calculates market price for EUR/BUSD
		aux_token = Token('EUR', 'BUSD', 0)
		eur_busd_price = BinanceAPI.market_price(aux_token)['price']

		# sets this market price to BUSD tokens
		# now BUSD tokens have EUR conversion price
		busd_token.set_price(float(eur_busd_price))

		TokenManager.add(busd_token)

	def fix_BETH_tokens(beth_token):
		# {"symbol": "BETH","pair": "BUSD","price": "0.0","spot_quantity": "0.00965173","earn_quantity": "0","balance": "0.0"}

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
		beth_token.set_price(beth_busd_price)

		TokenManager.add(beth_token)

	def fix_SHIB_tokens(shib_token):
		TokenManager.delete(shib_token) # SHIB2
		shib_token.set_symbol('SHIB')
		shib_token.update_token()
		TokenManager.add(shib_token) # SHIB


	def fix_tokens(tokens):
		if 'BETH' in tokens: SpecialTokens.fix_BETH_tokens(tokens['BETH'])
		if 'BUSD' in tokens: SpecialTokens.fix_BUSD_tokens(tokens['BUSD'])
		if 'SHIB2' in tokens: SpecialTokens.fix_SHIB_tokens(tokens['SHIB2'])

		return TokenManager.tokens()
