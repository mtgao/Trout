from itertools import permutations
from graph import Graph
from random import randint

def construct_path(min_count, g, src, dest):

	path = [src]
	latest = src
	for i in range(0, min_count):
		latest = g.findMinNode(latest, path, dest)
		path.append(latest)
	path.append(dest)
	return path

def main():

	members = ["Esh", "Michael", "Christine", "Sunil", "Hunter", "David", "Hannah", "Phil", "Adi", "Geuni"]
	g = Graph(members)
	for pair in permutations(members, 2):
		g.addEdge(pair, randint(1, 50))
	g.display()
	p = construct_path(5, g, "Hunter", "Hannah")
	for name in p:
		print name
		
if __name__ == "__main__":
	main()