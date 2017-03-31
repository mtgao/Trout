import sys, thread
import socket, select, pickle
import time
from message import Message
from membershiplist import Memberlist 

INTRODUCER_IP = '192.168.1.2'
UDP_PORT = 5005

class Node:
	introducer = 0

	def __init__(self, isIntroducer, user):
		self.user = user
		self.SELF_IP = get_ip()
		if(isIntroducer):
			introducer = 1
		self.memberlist = Memberlist(self.user, self.SELF_IP)
		self.pingAck = 0


	def join(self):
		print self.memberlist.members
		print('Attempting to join cluster...')
		m =  Message('join', self.memberlist, self.user + ':' + self.SELF_IP)
		sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockSend.sendto(pickle.dumps(m), (INTRODUCER_IP, UDP_PORT)) 

	def leave(self):
		print('Attempting to leave cluster...')
		m =  Message('leave', self.memberlist, self.user)
		sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockSend.sendto(pickle.dumps(m), (INTRODUCER_IP, UDP_PORT)) 

	def listen(self):

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.SELF_IP, UDP_PORT))

		while True:

			data, addr = sock.recvfrom(1024)
			m = pickle.loads(data)
			print('Received message:', m.header, m.content)

			if(m.header == 'join'):
				userInfo = m.content.split(':')  
				self.memberlist.addMember(userInfo[0], userInfo[1])
				self.memberlist.updateTime() 

				# send join ack so new member has latest list
				ackMessage =  Message('join-ack', self.memberlist, self.SELF_IP)
				sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sockSend.sendto(pickle.dumps(ackMessage), (userInfo[1], UDP_PORT)) 

			elif(m.header == 'join-ack'):
				print('ack received')
				self.memberlist.updateList(m.memberlist)

			elif(m.header == 'leave'):
				self.memberlist.removeMember(m.content)
				self.memberlist.updateTime()

			elif(m.header == 'ping'):
				self.memberlist.updateList(m.memberlist)

				# send a ping act for failure detection
				ackMessage =  Message('ping-ack', self.memberlist, self.SELF_IP)
				sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sockSend.sendto(pickle.dumps(ackMessage), (m.content, UDP_PORT)) 

			elif(m.header == 'ping-ack'):
				self.pingAck = 1

				# add a ping ack and we'll have a failure detector


			else:
				print 'bad message'

	# use SWIM style round robin pinging
	def ping(self):
		while True:
			for user in self.memberlist.members.keys():
				if user != self.user:
					time.sleep(1)
					m =  Message('ping', self.memberlist, self.SELF_IP)
					sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					sockSend.sendto(pickle.dumps(m), (self.memberlist.members[user], UDP_PORT)) 

					# timeout is 3 seconds from now
					timeout = time.time() + 3
					while True:
						if(self.pingAck == 1):
							#print 'ping ack received!'
							self.pingAck = 0
							break
						if(time.time() > timeout):
							print 'ping ack not received!'
							self.memberlist.removeMember(user)
							break



	def userIN(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		while True:
			command = sys.stdin.readline().strip()
			if(command == 'join'):
				self.join()
			elif(command == 'leave'):
				self.leave()
			elif(command == 'ping'):
				self.ping()
			elif(command == 'show'):
				print(self.memberlist.members)

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]



def main():
	if sys.argv[1] == '-i':
		print('Starting introducer node...')
		n = Node(1, sys.argv[2])
	else:
		n = Node(0, sys.argv[1]) 
		n.join() 

	thread.start_new_thread(n.listen, ())
	thread.start_new_thread(n.ping, ())

	n.userIN() 



if __name__ == "__main__":
	main() 