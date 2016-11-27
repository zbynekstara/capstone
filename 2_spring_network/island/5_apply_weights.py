# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('./4_plain/island.nod.xml', 'r')
edge_file = open('./4_plain/island.edg.xml', 'r')
dump_file = open('./3_dump/island.dump.xml', 'r')

weights_node_file = open('./5_weights/weights.nod.xml', 'w')
weights_edge_file = open('./5_weights/weights.edg.xml', 'w')
weights_dump_file = open('./5_weights/weights.dump.xml', 'w')

"""
location_list = [] # 1 # keep unchanged
node_list = [] # 8545 # input # output (modified)
edge_list = [] # 17909 # input
roundabout_list = [] # 79 # keep unchanged
edge_weight_list = [] # 17909 # input
"""

# READ NODE FILE TO GET NODES
print "read node file"
node_tree = ET.parse(node_file)
node_root = node_tree.getroot()

file_nodes = node_root.iter('node')
node_subtree = ET.Element('node_subtree_root')
node_len = 0
for file_node in file_nodes:
	node_subtree.append(file_node)
	node_len += 1
print str(node_len)

# READ EDGE FILE TO GET EDGES
print "read edge file"
edge_tree = ET.parse(edge_file)
edge_root = edge_tree.getroot()

file_edges = edge_root.iter('edge')
edge_subtree = ET.Element('edge_subtree_root')
edge_len = 0
for file_edge in file_edges:
	edge_subtree.append(file_edge)
	edge_len += 1
print str(edge_len)

# READ DUMP FILE TO GET EDGE WEIGHTS
print "read dump file"
dump_tree = ET.parse(dump_file)
dump_root = dump_tree.getroot().find('interval')

file_dump_edges = dump_root.iter('edge')
dump_edge_subtree = ET.Element('dump_edge_subtree_root')
dump_edge_len = 0
for file_dump_edge in file_dump_edges:
	dump_edge_subtree.append(file_dump_edge)
	dump_edge_len += 1
print str(dump_edge_len)

# DESIGNATE QUADRANTS
print "designate quadrants"
nodes = node_subtree.iter('node')
min_x = 0.0
max_x = 0.0
min_y = 0.0
max_y = 0.0
for node in nodes:
		node_x = float(node.get('x'))
		node_y = float(node.get('y'))

		if node_x < min_x:
			min_x = node_x
		elif node_x > max_x:
			max_x = node_x

		if node_y < min_y:
			min_y = node_y
		elif node_y > max_y:
			max_y = node_y

edges = edge_subtree.iter('edge')
dump_edges = dump_edge_subtree.iter('edge')
for edge in edges:
	dump_edge = next(dump_edges)
	print edge.get('id')+" "+dump_edge.get('id')
	assert edge.get('id') == dump_edge.get('id')

	edge_from = edge.get('from')
	edge_to = edge.get('to')

	node_from = node_subtree.find('node[@id=\''+edge_from+'\']')
	node_from_x = float(node_from.get('x'))
	node_from_y = float(node_from.get('y'))

	node_to = node_subtree.find('node[@id=\''+edge_to+'\']')
	node_to_x = float(node_to.get('x'))
	node_to_y = float(node_to.get('y'))

	edge_avg_x = (node_from_x+node_to_x)/2.0
	edge_avg_y = (node_from_y+node_to_y)/2.0

	bb_x_size = max_x-min_x
	bb_y_size = max_y-min_y

	edge_x_quadrant = int(((edge_avg_x-min_x)/bb_x_size)*10.0)
	if edge_x_quadrant == 10:
		edge_x_quadrant = 9

	edge_y_quadrant = int(((edge_avg_y-min_y)/bb_y_size)*10.0)
	if edge_y_quadrant == 10:
		edge_y_quadrant = 9

	edge_quadrant = edge_x_quadrant+(10*edge_y_quadrant)
	
	dump_edge.set('quadrant',str(edge_quadrant))
	#print str(edge_quadrant)

# APPLY WEIGHTS TO THE EDGES
print "apply weights to edges"
# assumes that the list of edges exactly matches the list of weighted edges
edges = edge_subtree.iter('edge')
dump_edges = dump_edge_subtree.iter('edge')
for edge in edges:
	# will end up with len, dump_speed, speed (=free_speed), slowdown, slowdown_ratio

	dump_edge = next(dump_edges)

	edge_from = edge.get('from')
	edge_to = edge.get('to')

	node_from = node_subtree.find('node[@id=\''+edge_from+'\']') # assumes that the node is present in node list
	node_from_x = float(node_from.get('x'))
	node_from_y = float(node_from.get('y'))
	node_to = node_subtree.find('node[@id=\''+edge_to+'\']') # assumes that the node is present in node list
	node_to_x = float(node_to.get('x'))
	node_to_y = float(node_to.get('y'))
	edge_len = math.hypot(abs(node_from_x-node_to_x),abs(node_from_y-node_to_y)) # hypotenuse
	edge.set('len',str(edge_len))

	dump_speed = float(dump_edge.get('speed',-1.0))
	edge.set('dump_speed',str(dump_speed))

	#desired length should be traveltime
	#weight should be real_speed = edgelen/traveltime #OR inverse of traveltime = 1/traveltime
	free_speed = float(edge.get('speed')) # free flow speed
	#dump_edge.set('free_speed',str(free_speed))

	#dump_speed = float(edge.get('dump_speed')) # speed with traffic
	if dump_speed == 0.00:
		# dump speed can be 0.00 - was not enough to be rounded to 0.01 but was not 0 either
		dump_speed = 0.004999
		# this produces problems when the graph is being generated
		# need to have a metric that takes the original length into account to preserve shapes
	if dump_speed == -1.0:
		# nodes that had no cars at all
		dump_speed = free_speed

	slowdown = free_speed - dump_speed
	#edge.set('diff_speed',str(diff_speed))
	#dump_edge.set('diff_speed',str(diff_speed))
	edge.set('slowdown',str(slowdown))

	slowdown_ratio = slowdown / free_speed # how much slower is traffic than it should be? 1 = no movement, 0 = same speed as free movement
	edge.set('slowdown_ratio',str(slowdown_ratio))
	dump_edge.set('slowdown_ratio', str(slowdown_ratio)) # needed for colormaps

"""
# APPLY WEIGHTS TO THE NODES
print "apply weights to nodes"
# for each node, add up weights from incoming edges
# actually follow edges because they are the ones that have connection info
# then divide by sum by number of incoming edges
edges = edge_subtree.iter('edge') # reset edges iter
for edge in edges:
	#if edge.get('to') is not None:
	node = node_subtree.find('node[@id=\''+edge.get('to')+'\']') # assumes that the node is present in node list
	node.set('weight_sum',str(float(node.get('weight_sum','0.0'))+float(edge.get('weight')))) # increase node's weight sum by edge's weight
	node.set('weight_num',str(float(node.get('weight_num','0.0'))+1.0)) # increment node's weight num
nodes = node_subtree.iter('node')
for node in nodes:
	node.set('weight',str(float(node.get('weight_sum','0.0'))/float(node.get('weight_num','1.0')))) # average or 0.0 if no data

# IDENTIFY NEIGHBORS
print "identify neighbors"
# identify nodes' neighbors and how to reach them
edges = edge_subtree.iter('edge') # reset edges iter
for edge in edges:
	source_node = node_subtree.find('node[@id=\''+edge.get('from')+'\']') # assumes that the source node is present in node list
	source_node.append(ET.Element('neighbor', attrib={'id':edge.get('to'),'edge':edge.get('id')})) # add the destination of the edge (edges store their id's) to a list of neighbors of the source node

# ADDED
# IDENTIFY CONNECTED NODES
print "identify connected"
# identify the nodes connected to nodes (reverse neighbors)
edges = edge_subtree.iter('edge') # reset edges iter
for edge in edges:
	target_node = node_subtree.find('node[@id=\''+edge.get('to')+'\']') # assumes that the target node is present in node list
	target_node.append(ET.Element('connected', attrib={'id':edge.get('from'),'edge':edge.get('id')})) # add the source of the edge to list of connected of the target node
"""

# WRITE OUTPUT FILES
print "write output files"
node_tree.write(weights_node_file,encoding='UTF-8',xml_declaration=True)
edge_tree.write(weights_edge_file,encoding='UTF-8',xml_declaration=True)
dump_tree.write(weights_dump_file,encoding='UTF-8',xml_declaration=True)

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()
dump_file.close()
weights_node_file.close()
weights_edge_file.close()
weights_dump_file.close()