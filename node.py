import sys, thread, os, signal
import socket, select, pickle
import time
from message import Message
from membershiplist import Memberlist 
from itertools import permutations
from graph import Graph
from random import randint

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
		m =  Message('join', self.memberlist, self.user + ':' + self.SELF_IP,[])
		sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockSend.sendto(pickle.dumps(m), (INTRODUCER_IP, UDP_PORT)) 

	def leave(self):
		print('Attempting to leave cluster...')
		os.kill(os.getpid(), signal.SIGUSR1)
#		m =  Message('leave', self.memberlist, self.user)
#		sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#		sockSend.sendto(pickle.dumps(m), (INTRODUCER_IP, UDP_PORT)) 

	def sendMessage(self, content, directions):
		print('Sending message...')
		print(directions) 
		directions.pop(0) 
		m = Message('message', self.memberlist, content, directions)
		sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockSend.sendto(pickle.dumps(m), (self.memberlist.members[directions[0]], UDP_PORT)) 

	def listen(self):

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.SELF_IP, UDP_PORT))

		while True:

			data, addr = sock.recvfrom(1024)
			m = pickle.loads(data)
			#print('Received message:', m.header, m.content)

			if(m.header == 'join'):
				userInfo = m.content.split(':')  
				self.memberlist.addMember(userInfo[0], userInfo[1])
				self.memberlist.updateTime() 

				# send join ack so new member has latest list
				ackMessage =  Message('join-ack', self.memberlist, self.SELF_IP,[])
				sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sockSend.sendto(pickle.dumps(ackMessage), (userInfo[1], UDP_PORT)) 

			elif(m.header == 'join-ack'):
				print('ack received')
				self.memberlist.forceUpdateList(m.memberlist)

			elif(m.header == 'leave'):
				self.memberlist.removeMember(m.content)
				self.memberlist.updateTime()

			elif(m.header == 'ping'):
				self.memberlist.updateList(m.memberlist)

				# send a ping act for failure detection
				ackMessage =  Message('ping-ack', self.memberlist, self.SELF_IP,[])
				sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sockSend.sendto(pickle.dumps(ackMessage), (m.content, UDP_PORT)) 

			elif(m.header == 'ping-ack'):
				self.pingAck = 1

			elif(m.header == 'message'):
				print('message received')
				print(m.directions)
				if(not m.directions):
					print(m.content) 
				else:
					nextNode = m.directions.pop(0)
					m = Message('message', self.memberlist, m.content, m.directions)
					sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					sockSend.sendto(pickle.dumps(m), (self.memberlist.members[nextNode], UDP_PORT))

			else:
				print 'bad message'

	# use SWIM style round robin pinging
	def ping(self):
		while True:
			for user in self.memberlist.members.keys():
				if user != self.user:
					time.sleep(1)
					m =  Message('ping', self.memberlist, self.SELF_IP,[])
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
			elif(command == 'send'):
				members = self.memberlist.members.keys() 
				g = Graph(members)
				for pair in permutations(members, 2):
					g.addEdge(pair, randint(1, 50))
				g.display()
				directions = construct_path(0, g, "michael", "esh")
				self.sendMessage('hellloooo', directions) 

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

def construct_path(min_count, g, src, dest):

	path = [src]
	latest = src
	for i in range(0, min_count):
		latest = g.findMinNode(latest, path, dest)
		path.append(latest)
	path.append(dest)
	return path


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
