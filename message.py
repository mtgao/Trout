import time

class Message: 
	def __init__(self, type, memberlist, data, list):
		self.header = type
		self.timestamp = time.strftime('%H:%M:%S')
		self.memberlist = memberlist
		self.content = data
		self.directions = list
	
