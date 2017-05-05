import time

class Memberlist:

	def __init__(self, user = None, IP = None):
		self.timestamp = time.strftime('%H:%M:%S')
		self.members = {user:IP}

	def addMember(self, user, IP):
		self.members[user] = IP 

	def removeMember(self, user):
		del self.members[user]

	def updateTime(self):
		self.timestamp = time.strftime('%H:%M:%S')

	def updateList(self, otherList):
		# update our membership list if other list contains more recent timestamp
		if(self.timestamp < otherList.timestamp):
			self.members = otherlist.members 
			self.timestamp = otherlist.timestamp 
			
	def forceUpdateList(self, otherList): 
		self.members = otherlist.members 
		self.timestamp = otherlist.timestamp 