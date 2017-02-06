# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET

node_file = open('F:\Capstone\AUH\osm\plain\island.nod.xml', 'r') # sys.argv[1] F:\Capstone\AUH\osm\plain\island.nod.xml
edge_file = open('F:\Capstone\AUH\osm\plain\island.edg.xml', 'r') # sys.argv[2] F:\Capstone\AUH\osm\plain\island.edg.xml
dump_file = open('F:\Capstone\AUH\osm\duarouter\island.dump.xml', 'r') # sys.argv[3] F:\Capstone\AUH\osm\duarouter\island.dump.xml
gravity_file = open('F:\Capstone\AUH\osm\output\island.gravity.xml', 'w') # F:\Capstone\AUH\osm\output\island.gravity.xml

"""location_list = [] # 1 # keep unchanged
node_list = [] # 8545 # input # output (modified)
edge_list = [] # 17909 # input
roundabout_list = [] # 79 # keep unchanged
edge_weight_list = [] # 17909 # input

weighted_edge_list = []
weighted_node_list = []"""

# READ NODE FILE TO GET NODES
tree = ET.parse(node_file)
root = tree.getroot()
location_list = root.findall('location')
node_list = root.findall('node')
print(len(location_list))
print(len(node_list))

# READ EDGE FILE TO GET EDGES
tree = ET.parse(edge_file)
root = tree.getroot()
edge_list = root.findall('edge')
roundabout_list = root.findall('roundabout')
print(len(edge_list))
print(len(roundabout_list))

# READ DUMP FILE TO GET EDGE WEIGHTS
tree = ET.parse(dump_file)
root = tree.getroot()
edge_weight_list = root.findall('./interval/edge')
print(len(edge_weight_list))

# APPLY WEIGHTS TO THE EDGES
# assumes that the list of edges exactly matches the list of edge weights
# is occupancy even the right measure here?
weighted_edge_list = list(edge_list) # clone original edge list
index = 0
while index < len(edge_list):
	weight = edge_weight_list[index].get('occupancy')
	if weight == None:
		weight = 0.0
	weight = float(weight)
	if weight > 100.0: # is this necessary? how can occupancy be >100% though?
		weight = 100.0
	weighted_edge_list[index].set('weight', weight)
	index += 1

# APPLY WEIGHTS TO THE NODES
# for each node, add up weights from incoming edges
# actually follow edges because they are the ones that have connection info
# then divide by sum by number of incoming edges
weighted_node_list = list(node_list) # clone original node list
for weighted_edge in weighted_edge_list:
	weighted_node = weighted_node_list.find('node[@id=\''+weighted_edge.get('to')+'\'') # assumes that the node is present in node list
	weighted_node.set('weight_sum',weighted_node.get('weight_sum',0.0)+weighted_edge.get('weight')) # increase node's weight sum by edge's weight
	weighted_node.set('weight_num',weighted_node.get('weight_num',0.0)+1.0) # increment node's weight num
for weighted_node in weighted_node_list:
	weighted_node.set('weight',weighted_node.get('weight_sum',0.0)/weighted_node.get('weight_num',1.0)) # average or 0.0 if no data

# GET AVERAGE WEIGHT
# add up all weights and divide by number of nodes
# maybe not necessary?
node_weight_sum = 0.0
for weighted_node in weighted_node_list:
	node_weight_sum += weighted_node.get('weight',0.0)
average_weight = node_weight_sum/float(len(weighted_node_list))

# IDENTIFY OUTGOING EDGES AND NEIGHBORS
# identify nodes' outgoing(!) edges
# also identify nodes' neighbors (through outgoing nodes!)
for edge in weighted_edge_list:
	source_node = weighted_node_list.find('node[@id=\''+edge.get('from')+'\'') # assumes that the source node is present in node list
	source_node.append(ET.Element('outgoing_edge', attrib={'id',edge.get('id')})) # add the edge to list of outgoing edges of the source node
	source_node.append(ET.Element('neighbor', attrib={'id',edge.get('from')})) # add the destination of the edge (edges store their id's) to a list of neighbors of the source node

#def get_gravity_positions(weighted_junctions, average_weight):
# list of junctions for gravity file with new positions
# edge geometry positions have to change too
# everything that does not include positions can be copied from net
#return gravity_positions

gravity_file.write("Hello world")

node_file.close()
edge_file.close()
dump_file.close()
gravity_file.close()