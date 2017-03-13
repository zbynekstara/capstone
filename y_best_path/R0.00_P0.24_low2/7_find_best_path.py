# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET
import argparse

# OPEN FILES
print "open files"

node_file = open('./6_prepared/modified.nod.xml', 'r')
edge_file = open('./6_prepared/modified.edg.xml', 'r')

# OPTION PARSER
print "option parser"
parser = argparse.ArgumentParser(description='Finds best path')

parser.add_argument('start_node', help='start node')
parser.add_argument('target_node', help='target node')
parser.add_argument('supplied_path', help='supplied path')

args = parser.parse_args()

# READ NODE FILE TO GET NODES
print "read node file"

class Node:
	def __init__(self, name):
		self.name = name

		split_name = name.split('x')
		self.x_pos = (split_name[0].split('_'))[1]
		self.y_pos = split_name[1]

		self.cost = float("inf") # how hard is it to get here from start
		self.came_from = None # a Node this node can be reached from most efficiently
		self.came_through = None # an Edge used to reach this node from cameFrom
		self.connected_edges = [] # Edges that go from this node
		#self.neighbors = [] # Nodes reachable from this node, assumes that order of neighbors is the same as order of connected edges!!

	def add_connected_edge(self, edge):
		self.connected_edges.append(edge)

	"""def add_neighbor(self, node):
		self.neighbors.append(node)"""

	def set_cost(self, node, edge):
		new_cost = node.cost + edge.time_cost
		if new_cost < self.cost:
			self.cost = new_cost
			self.came_from = node
			self.came_through = edge

node_tree = ET.parse(node_file)
node_root = node_tree.getroot()

file_nodes = node_root.iter('node')
nodes = []
for file_node in file_nodes:
	nodes.append(Node(file_node.get('id')))

# READ EDGE FILE TO GET EDGES
print "read edge file"

def find_node(nodes, name):
	for node in nodes:
		if node.name == name:
			return node
	raise Exception("Node cannot be found; incongruous node definition")

class Edge:
	def __init__(self, name, dump_speed, length, from_string, to_string):
		self.name = name
		self.time_cost = length/dump_speed

		self.from_node = find_node(nodes, from_string)
		self.to_node = find_node(nodes, to_string)

		self.from_node.add_connected_edge(self)
		#self.from_node.add_neighbor(self.to_node)

edge_tree = ET.parse(edge_file)
edge_root = edge_tree.getroot()

file_edges = edge_root.iter('edge')
edges = []
for file_edge in file_edges:
	edges.append(Edge(file_edge.get('id'), float(file_edge.get('dump_speed')), float(file_edge.get('len')), file_edge.get('from'), file_edge.get('to')))

# DIJKSTRA
print "dijkstra"

def find_min_cost_node(nodes):
	min_cost_node_index = 0
	min_cost = float("inf")
	index = 0
	while index < len(nodes):
		current_cost = nodes[index].cost
		if current_cost < min_cost:
			min_cost = current_cost
			min_cost_node_index = index
		index += 1
	return min_cost_node_index

start_node_name = "node_"+args.start_node
target_node_name = "node_"+args.target_node

start_node = find_node(nodes, start_node_name)
start_node.cost = 0

target_node = find_node(nodes, target_node_name)

unvisited_nodes = set()
for node in nodes:
	unvisited_nodes.add(node)

nodes_to_explore = []
nodes_to_explore.append(start_node)

while len(nodes_to_explore) > 0:
	current_node = nodes_to_explore.pop(find_min_cost_node(nodes_to_explore))
	if current_node not in unvisited_nodes:
		continue

	print "exploring "+current_node.name+", cost: "+str(current_node.cost)+", connected edges: "+str(len(current_node.connected_edges))
	if current_node.name == target_node.name:
		break

	for connected_edge in current_node.connected_edges:
		connected_node = connected_edge.to_node
		print "\texploring connected "+connected_edge.name+" connecting to "+connected_node.name
		if connected_node in unvisited_nodes:
			connected_node.set_cost(current_node, connected_edge)
			nodes_to_explore.append(connected_node)

	unvisited_nodes.remove(current_node)

best_nodes_sequence = []
#best_edges_sequence = []
best_path_length = 0.0

current_node = target_node
while current_node.came_from is not None:
	best_nodes_sequence.insert(0, current_node)
	#best_edges_sequence.insert(0, current_node.came_through)
	best_path_length += current_node.came_through.time_cost

	current_node = current_node.came_from

best_nodes_sequence.insert(0, current_node)

print ""

print "evaluation of supplied path:"
def find_edge(from_node, to_node):
	for edge in from_node.connected_edges:
		if edge.to_node == to_node:
			return edge
	raise Exception("Edge cannot be found; incongruous path")

supplied_path = args.supplied_path

supplied_path_length = float("inf")
if supplied_path != "None":
	supplied_node_codes = supplied_path.split(",")

	supplied_path_nodes = []
	current_node = None
	previous_node = None
	supplied_path_length = 0
	for supplied_node_code in supplied_node_codes:
		current_node = find_node(nodes,"node_"+supplied_node_code)
		supplied_path_nodes.append(current_node)
		
		if previous_node is not None:
			connecting_edge = find_edge(previous_node, current_node)
			supplied_path_length += connecting_edge.time_cost

		print "\t"+current_node.name

		previous_node = current_node

	if supplied_path_nodes[0] is not start_node:
		raise Exception("Start of supplied path is not the same as start node")
	if supplied_path_nodes[-1] is not target_node:
		raise Exception("Target of supplied path is not the same as target node")
else:
	print "\t<none>"

print ""
print "best path nodes sequence:"
for print_node in best_nodes_sequence:
	print "\t"+print_node.name

"""print "best path edges sequence:"
for print_edge in best_edges_sequence:
	print "\t"+print_edge.name"""

print ""

print "total best path time cost: "+str(best_path_length)

if supplied_path == "None":
	print "no path was supplied for comparison"
else:
	print "total supplied path time cost: "+str(supplied_path_length)

	path_length_difference = supplied_path_length-best_path_length
	path_length_slowdown_ratio = (supplied_path_length/best_path_length)-1
	path_length_slowdown_percentage = path_length_slowdown_ratio*100

	print "\tsupplied path is "+str(path_length_difference)+" more costly"
	print "\tsupplied path is "+str(path_length_slowdown_percentage)+" % more costly"

print ""

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()