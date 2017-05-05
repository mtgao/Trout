from operator import itemgetter

class Graph:

	def __init__(self, nodes):

		self.vertices = nodes 
		self.edges = {}
		self.adj_weights = {}

	def addEdge(self, endpoints, num):

		self.edges[endpoints] = num
		if endpoints[0] not in self.adj_weights:
			pair = [(num, endpoints[1])]
			self.adj_weights[endpoints[0]] = pair
		else:
			pair = (num, endpoints[1])
			self.adj_weights[endpoints[0]].append(pair)

	def edgeWeight(self, endpoints):

		return self.edges[endpoints]

	def findMinNode(self, cur, seenNodes, des):

		adj = self.adj_weights[cur]
		s_adj = sorted(adj,key=itemgetter(0))
		for pair in s_adj:
			if pair[1] not in seenNodes and pair[1] != des:
				return pair[1]

	def display(self):

		print "The edges in this graph with their respective weights are: "
		for v in self.vertices:
			adj = self.adj_weights[v]
			s_adj = sorted(adj,key=itemgetter(0))
			for pair in s_adj:
				print "(" + v + "," + pair[1] + ") -> " + str(pair[0])