class Utils:
	def calculate_balances(tokens):
		spot_balance  = float(0)
		earn_balance  = float(0)
		global_balance = float(0)

		for e in tokens:
			spot_balance += tokens[e].spot_balance()
			earn_balance += tokens[e].earn_balance()
			global_balance += tokens[e].global_balance()

		balances = Utils.convert_balances_to_EUR([spot_balance, earn_balance, global_balance], tokens['BUSD'].price())
		return {'spot': balances[0], 'earn': balances[1], 'global': balances[2]}

	def convert_balance_to_EUR(balance, busd_price):
		# tokens['BUSD'] have EUR conversion price
		return float(balance) / float(busd_price)

	def convert_balances_to_EUR(balances, busd_price):
		result = []
		for e in balances: result.append(Utils.convert_balance_to_EUR(e, busd_price))

		return result
