class Message: 
	def __init__(self, type, memberlist, data):
		self.header = type
		self.memberlist = memberlist
		self.content = data
	
