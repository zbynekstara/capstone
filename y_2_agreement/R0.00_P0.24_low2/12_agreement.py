# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET
import argparse

# OPEN FILES
print "open files"

node_file = open('./6_prepared/modified.nod.xml', 'r')
edge_file = open('./6_prepared/modified.edg.xml', 'r')
path_file = open('./11_paths/paths.txt', 'r')

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

# READ PATH FILE
print "read path file"
path_lines = path_file.readlines()
path_len = len(paths)

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

print str(path_len)

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()
path_file.close()