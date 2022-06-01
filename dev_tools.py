import datetime
class Performance:
	_start_time = None
	_end_time = None

	def measure(callback):
		Performance._start_time = datetime.datetime.now()
		callback()
		Performance._end_time = datetime.datetime.now()

		return Performance._end_time - Performance._start_time
