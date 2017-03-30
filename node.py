import sys
import socket
import thread
import pickle
import time
from message import Message
from membershiplist import Memberlist 

INTRODUCER_IP = '192.168.1.2'
UDP_PORT = 5005

class Node:
	introducer = 0

	def __init__(self, isIntroducer):
		self.SELF_IP = get_ip()
		if(isIntroducer):
			introducer = 1
		self.memberlist = Memberlist(self.SELF_IP)
		

	def join(self):
		print self.memberlist.members
		print('Attempting to join cluster...')
		m =  Message('join', self.memberlist, self.SELF_IP)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(pickle.dumps(m), (INTRODUCER_IP, UDP_PORT)) 

	def leave(self):
		print('Attempting to leave cluster...')
		m =  Message('leave', self.memberlist, self.SELF_IP)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(pickle.dumps(m), (INTRODUCER_IP, UDP_PORT)) 

	def listen(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.SELF_IP, UDP_PORT))
		while True:
			data, addr = sock.recvfrom(1024)
			m = pickle.loads(data)
			print('Received message:', m.content)

			if(m.header == 'join'):
				self.memberlist.addMember(m.content)
				self.memberlist.updateTime() 
			elif(m.header == 'leave'):
				self.memberlist.removeMember(m.content)
				self.memberlist.updateTime()
				print self.memberlist.members
			elif(m.header == 'ping'):
				self.memberlist.updateList(m.memberlist)
				print self.memberlist.timestamp
			else:
				print 'bad message'

	# use SWIM style round robin pinging
	def ping(self):
		while True:
			for IP in self.memberlist.members:
				time.sleep(1)
				m =  Message('ping', self.memberlist, self.SELF_IP)
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.sendto(pickle.dumps(m), (IP, UDP_PORT)) 


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
	if sys.argv[1:] == ['-i']:
		print('Starting introducer node...')
		n = Node(1)
	else:
		n = Node(0) 
		n.join() 

	thread.start_new_thread(n.listen, ())

	n.userIN() 



if __name__ == "__main__":
	main() 