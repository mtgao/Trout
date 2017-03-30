import time

class Message: 
	def __init__(self, type, memberlist, data):
		self.header = type
		self.timestamp = time.strftime('%H:%M:%S')
		self.memberlist = memberlist
		self.content = data
	
