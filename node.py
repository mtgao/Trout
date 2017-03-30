import sys
import socket
import multiprocessing 
import pickle
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
			

	def userIN(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		while True:
			if(sys.stdin.readline().strip() == 'join'):
				self.join()

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

	listener = multiprocessing.Process(target=n.listen)
	listener.start()

	n.userIN() 




if __name__ == "__main__":
	main() 