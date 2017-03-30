class Message: 
	def __init__(self, type, data):
		self.header = type
		self.content = data
