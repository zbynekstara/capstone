# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET
import argparse

# OPEN FILES
print "open files"

node_file_list = []
edge_file_list = []

node_file_list.append(open('./1_1/6_prepared/modified.nod.xml', 'r')) # dense high
edge_file_list.append(open('./1_1/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./1_2/6_prepared/modified.nod.xml', 'r')) # dense mid
edge_file_list.append(open('./1_2/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./1_3/6_prepared/modified.nod.xml', 'r')) # dense low
edge_file_list.append(open('./1_3/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./2_1/6_prepared/modified.nod.xml', 'r')) # mid high
edge_file_list.append(open('./2_1/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./2_2/6_prepared/modified.nod.xml', 'r')) # mid mid
edge_file_list.append(open('./2_2/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./2_3/6_prepared/modified.nod.xml', 'r')) # mid low
edge_file_list.append(open('./2_3/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./3_1/6_prepared/modified.nod.xml', 'r')) # sparse high
edge_file_list.append(open('./3_1/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./3_2/6_prepared/modified.nod.xml', 'r')) # sparse mid
edge_file_list.append(open('./3_2/6_prepared/modified.edg.xml', 'r'))
node_file_list.append(open('./3_3/6_prepared/modified.nod.xml', 'r')) # sparse low
edge_file_list.append(open('./3_3/6_prepared/modified.edg.xml', 'r'))

input_paths_file = open('./paths.csv','r')
# order: 3x de-hi-di, de-hi-go, de-mi-di, de-mi-go etc

adjusted_paths_file = open('./adjusted_paths.csv','w')
#boolean_paths_file = open('./boolean_paths.csv','w')
best_paths_file = open('./best_paths.csv','w')
best_path_lengths_file = open('./best_path_lengths.csv','w')
accuracy_paths_file = open('./accuracy_paths.csv','w')

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

	def reset_cost(self):
		self.cost = float("inf")
		self.came_from = None
		self.came_through = None

def find_node(nodes, name):
	for node in nodes:
		if node.name == name:
			return node
	print name
	raise Exception("Node cannot be found; incongruous node definition")

class Edge:
	def __init__(self, nodes, name, dump_speed, length, from_string, to_string):
		self.name = name
		self.time_cost = length/dump_speed

		self.from_node = find_node(nodes, from_string)
		self.to_node = find_node(nodes, to_string)

		self.from_node.add_connected_edge(self)
		#self.from_node.add_neighbor(self.to_node)

nodes_list = []
edges_list = []
f_counter = 0
while f_counter < 9:
	# READ NODE FILE TO GET NODES
	print "read node file"

	node_tree = ET.parse(node_file_list[f_counter])
	node_root = node_tree.getroot()

	file_nodes = node_root.iter('node')
	nodes = []
	for file_node in file_nodes:
		nodes.append(Node(file_node.get('id')))
	nodes_list.append(nodes)

	# READ EDGE FILE TO GET EDGES
	print "read edge file"

	edge_tree = ET.parse(edge_file_list[f_counter])
	edge_root = edge_tree.getroot()

	file_edges = edge_root.iter('edge')
	edges = []
	for file_edge in file_edges:
		edges.append(Edge(nodes, file_edge.get('id'), float(file_edge.get('dump_speed')), float(file_edge.get('len')), file_edge.get('from'), file_edge.get('to')))
	edges_list.append(edges)

	f_counter += 1

# PATHS ADJUSTMENT
print "adjusting paths file"
# take the simplified system, split into columns, strip quotation marks from columns, split into data points, and add zeros to node indices where necessary
# returns a list of path columns - which is a list of paths - itself a list of nodes (changed to have initial zeroes in indices when necessary)

input_path_columns = input_paths_file.readlines()
path_columns = []
for input_path_column in input_path_columns:
	path_column = input_path_column.strip("\n")
	
	input_paths = path_column.replace("\",\"",";").split(';')
	paths = []
	for input_path in input_paths:
		input_path_raw = input_path.strip("\"")
		
		input_path = input_path_raw.split(',')
		#print input_path
		path = []
		for input_node in input_path:
			node = ""
			indices = input_node.split('x')
			if len(indices[0]) == 1:
				node += "0"
			node += indices[0]
			node += "x"
			if len(indices[1]) == 1:
				node += "0"
			node += indices[1]
			path.append(node)

		paths.append(path)

	path_columns.append(paths)

# ENDPOINT DETECTION
print "detecting endpoints of paths"
# for each column, get the first and last nodes to determine endpoints

#print str(path_columns)

start_nodes = []
target_nodes = []
for path_column in path_columns:
	start_node = path_column[0][0] # first node of the first path in column
	target_node = path_column[0][-1] # last node of the first path in column

	start_nodes.append(start_node)
	target_nodes.append(target_node)

#print str(start_nodes)
#print str(target_nodes)

def refresh_nodes():
	for nodes in nodes_list:
		for node in nodes:
			node.reset_cost()

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

best_paths = []
best_path_lengths = []
counter = 0
while counter < len(path_columns):
# DIJKSTRA
	print "dijkstra"
	# for each column, find the best path

	refresh_nodes()

	current_nodes_list_index = int(counter/2) % 9
	nodes = nodes_list[current_nodes_list_index]

	#print str(counter)
	#print str(current_nodes_list_index)

	start_node_name = "node_"+start_nodes[counter]
	target_node_name = "node_"+target_nodes[counter]

	#print start_node_name
	#print target_node_name

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

		#if counter == 36: print "exploring "+current_node.name+", cost: "+str(current_node.cost)+", connected edges: "+str(len(current_node.connected_edges))
		if current_node.name == target_node.name:
			break

		for connected_edge in current_node.connected_edges:
			connected_node = connected_edge.to_node
			#if counter == 36: print "\texploring connected "+connected_edge.name+" connecting to "+connected_node.name
			if connected_node in unvisited_nodes:
				connected_node.set_cost(current_node, connected_edge)
				nodes_to_explore.append(connected_node)

		unvisited_nodes.remove(current_node)

	best_nodes_sequence = []
	#best_edges_sequence = []
	best_path_length = 0.0

	current_node = target_node
	while current_node.came_from is not None:
		#print "\t"+current_node.name
		best_nodes_sequence.insert(0, current_node)
		#best_edges_sequence.insert(0, current_node.came_through)
		best_path_length += current_node.came_through.time_cost

		current_node = current_node.came_from

	best_nodes_sequence.insert(0, current_node)

	print ""

	best_paths.append(best_nodes_sequence)
	best_path_lengths.append(best_path_length)

	counter += 1

# FILLING IN PATH ELEMENTS
print "filling in path elements"
# for each path, fill in the nodes on the way to each turn

adjusted_path_columns = []
for path_column in path_columns:
	adjusted_paths = []
	for path in path_column:
		adjusted_path = []	
		previous_node = None;
		counter = 0
		print str(path)
		for node in path:
			if counter == 0:
				adjusted_path.append(node)
				counter += 1
				previous_node = node
				continue

			previous_node_indices = previous_node.split('x')
			current_node_indices = node.split('x')

			current_node_x = int(current_node_indices[0])
			current_node_y = int(current_node_indices[1])
			previous_node_x = int(previous_node_indices[0])
			previous_node_y = int(previous_node_indices[1])

			horizontal_diff = current_node_x - previous_node_x
			vertical_diff = current_node_y - previous_node_y
			if horizontal_diff != 0: # horizontal segment
				if vertical_diff != 0:
					raise Exception("Diagonal movement")
				if horizontal_diff < -1: # moving to the left and we need to add extra nodes
					while horizontal_diff < -1:
						new_node_x = str(current_node_x-horizontal_diff-1)
						if len(new_node_x) == 1:
							new_node_x = "0"+new_node_x
						new_node_y = str(current_node_y)
						if len(new_node_y) == 1:
							new_node_y = "0"+new_node_y
						new_node = new_node_x+"x"+new_node_y

						adjusted_path.append(new_node)
						horizontal_diff += 1

				elif horizontal_diff > 1: # moving to the right and we need to add extra nodes
					while horizontal_diff > 1:
						new_node_x = str(current_node_x-horizontal_diff+1)
						if len(new_node_x) == 1:
							new_node_x = "0"+new_node_x
						new_node_y = str(current_node_y)
						if len(new_node_y) == 1:
							new_node_y = "0"+new_node_y
						new_node = new_node_x+"x"+new_node_y

						adjusted_path.append(new_node)
						horizontal_diff -= 1

			elif vertical_diff != 0: # vertical segment
				if vertical_diff < -1: # moving up and we need to add extra nodes
					while vertical_diff < -1:
						new_node_x = str(current_node_x)
						if len(new_node_x) == 1:
							new_node_x = "0"+new_node_x
						new_node_y = str(current_node_y-vertical_diff-1)
						if len(new_node_y) == 1:
							new_node_y = "0"+new_node_y
						new_node = new_node_x+"x"+new_node_y

						adjusted_path.append(new_node)
						vertical_diff += 1

				elif vertical_diff > 1: # moving down and we need to add extra nodes
					while vertical_diff > 1:
						new_node_x = str(current_node_x)
						if len(new_node_x) == 1:
							new_node_x = "0"+new_node_x
						new_node_y = str(current_node_y-vertical_diff+1)
						if len(new_node_y) == 1:
							new_node_y = "0"+new_node_y
						new_node = new_node_x+"x"+new_node_y

						adjusted_path.append(new_node)
						vertical_diff -= 1

			adjusted_path.append(node)
			counter += 1
			previous_node = node

		adjusted_paths.append(adjusted_path)

	adjusted_path_columns.append(adjusted_paths)

def find_edge(from_node, to_node):
	for edge in from_node.connected_edges:
		if edge.to_node == to_node:
			return edge
	print from_node.name
	print to_node.name
	raise Exception("Edge cannot be found; incongruous path")

supplied_path_column_lengths = []
path_column_length_differences = []
path_column_length_slowdown_ratios = []
column_counter = 0
for path_column in adjusted_path_columns:
	current_nodes_list_index = int(column_counter/2) % 9
	nodes = nodes_list[current_nodes_list_index]

	supplied_path_lengths = []
	path_length_differences = []
	path_length_slowdown_ratios = []
	for path in path_column:
		# EVALUATE PATH
		print "evaluation of supplied path:"
		# for each path, evaluate how much worse it is than the optimal path

		print path
		print column_counter
		print current_nodes_list_index

		supplied_path_nodes = path
		print "/"+supplied_path_nodes[0]+"/"
		print "/"+start_nodes[column_counter]+"/"
		if supplied_path_nodes[0] != start_nodes[column_counter]:
			raise Exception("Start of supplied path is not the same as start node")
		if supplied_path_nodes[-1] != target_nodes[column_counter]:
			raise Exception("Target of supplied path is not the same as target node")

		supplied_path_length = 0
		counter = 0
		previous_node = None
		for node in path:
			if counter == 0:
				counter += 1
				previous_node = node
				continue

			connecting_edge = find_edge(find_node(nodes,"node_"+previous_node), find_node(nodes,"node_"+node))
			supplied_path_length += connecting_edge.time_cost

			counter += 1
			previous_node = node

		supplied_path_lengths.append(supplied_path_length)

		print ""
		#print "best path nodes sequence:"
		best_nodes_sequence = best_paths[column_counter]
		for print_node in best_nodes_sequence:
			#print "\t"+print_node.name
			pass

		print ""

		best_path_length = best_path_lengths[column_counter]
		print "total best path time cost: "+str(best_path_length)

		print "total supplied path time cost: "+str(supplied_path_length)

		path_length_difference = supplied_path_length-best_path_length
		path_length_slowdown_ratio = (supplied_path_length/best_path_length)#-1 # the length in terms of best path length
		#path_length_slowdown_percentage = path_length_slowdown_ratio*100

		print "\tsupplied path is "+str(path_length_difference)+" more costly"
		#print "\tsupplied path is "+str(path_length_slowdown_percentage)+" % more costly"

		print ""

		path_length_differences.append(path_length_difference)
		path_length_slowdown_ratios.append(path_length_slowdown_ratio)

	supplied_path_column_lengths.append(supplied_path_lengths)
	path_column_length_differences.append(path_length_differences)
	path_column_length_slowdown_ratios.append(path_length_slowdown_ratios)
	column_counter += 1

# WRITE FILES
print "write files"

# adjusted paths file:
column_counter = 0
for adjusted_path_column in adjusted_path_columns:
	if column_counter != 0:
		adjusted_paths_file.write("\n")

	counter = 0
	for adjusted_path in adjusted_path_column:
		if counter != 0:
			adjusted_paths_file.write(",")
		adjusted_paths_file.write("\"")

		node_counter = 0
		for print_node in adjusted_path:
			if node_counter != 0:
				adjusted_paths_file.write(",")

			adjusted_paths_file.write(print_node)
			node_counter += 1

		adjusted_paths_file.write("\"")
		counter += 1

	column_counter += 1

# best paths file:
column_counter = 0
for best_path in best_paths:
	if column_counter != 0:
		best_paths_file.write("\n")
	best_paths_file.write("\"")

	counter = 0
	for print_node in best_path:
		if counter != 0:
			best_paths_file.write(",")

		best_paths_file.write(print_node.name.split('_')[1])
		counter += 1

	best_paths_file.write("\"")
	column_counter += 1

# best path lengths file:
column_counter = 0
for best_path_length in best_path_lengths:
	if column_counter != 0:
		best_path_lengths_file.write("\n")

	best_path_lengths_file.write(str(best_path_length))
	column_counter += 1

# accuracy paths file:
column_counter = 0
for path_length_slowdown_ratios in path_column_length_slowdown_ratios:
	if column_counter != 0:
		accuracy_paths_file.write("\n")

	node_counter = 0
	for path_length_slowdown_ratio in path_length_slowdown_ratios:
		if node_counter != 0:
			accuracy_paths_file.write(",")

		accuracy_paths_file.write(str(path_length_slowdown_ratio))
		node_counter += 1

	column_counter += 1

# CLOSE FILES
print "close files"

for node_file in node_file_list:
	node_file.close()
for edge_file in edge_file_list:
	edge_file.close()

input_paths_file.close()

adjusted_paths_file.close()
#boolean_paths_file.close()
best_paths_file.close()
best_path_lengths_file.close()
accuracy_paths_file.close()