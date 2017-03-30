import time

class Memberlist:

	def __init__(self, IP = None):
		self.timestamp = time.strftime('%H:%M:%S')
		self.members = set([IP]) 

	def addMember(self, IP):
		self.members.add(IP)

	def removeMember(self, IP):
		self.members.discard(IP)

	def updateTime(self):
		self.timestamp = time.strftime('%H:%M:%S')

	def updateList(self, otherList):
		# update our membership list if other list contains more recent timestamp
		if(self.timestamp < otherList.timestamp):
			self.members = otherlist.members 
			self.timestamp = otherlist.timestamp 
