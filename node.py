import sys
import socket
import multiprocessing 

INTRODUCER_IP = '192.168.1.2'
SELF_IP = '127.0.0.1'
UDP_PORT = 5005

class Node:
	introducer = 0

	def __init__(self, isIntroducer):
		if(isIntroducer):
			introducer = 1

	def join(self):
		print('Attempting to join cluster...')

	def leave(self):
		print('Attempting to leave cluster...')

	def listen(self):
		print('listening') 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((SELF_IP, UDP_PORT))
		while True:
			data, addr = sock.recvfrom(1024)
			print('Received message:', data)

	def userIN(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		while True:
			if(sys.stdin.readline().strip() == 'join'):
				sock.sendto("hi i'd like to join this cluster", (SELF_IP, UDP_PORT)) 



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