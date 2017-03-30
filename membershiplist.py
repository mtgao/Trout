import datetime

class Memberlist:

	def __init__(self, IP = None):
		self.timestamp = '{:%H:%M:%S}'.format(datetime.datetime.now())
		self.members = set([IP]) 