



class User(threading.Thread):

	def __init__(self, userid):


	def run(self):
		while(not self._stop):

			time.sleep(self._thinktime)