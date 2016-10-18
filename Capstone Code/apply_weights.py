# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('C:\Users\zs633\Capstone\AUH\osm\plain\island.nod.xml', 'r') # sys.argv[1] F:\Capstone\AUH\osm\plain\island.nod.xml
edge_file = open('C:\Users\zs633\Capstone\AUH\osm\plain\island.edg.xml', 'r') # sys.argv[2] F:\Capstone\AUH\osm\plain\island.edg.xml
dump_file = open('C:\Users\zs633\Capstone\AUH\osm\duarouter\island.dump.xml', 'r') # sys.argv[3] F:\Capstone\AUH\osm\duarouter\island.dump.xml

weights_node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\weights.nod.xml', 'w') # F:\Capstone\AUH\osm\output\weights.nod.xml
weights_edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\weights.edg.xml', 'w') # F:\Capstone\AUH\osm\output\weights.edg.xml

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

# APPLY WEIGHTS TO THE EDGES
print "apply weights to edges"
# assumes that the list of edges exactly matches the list of weighted edges
# is occupancy even the right measure here?
dump_edges = dump_edge_subtree.iter('edge')
edges = edge_subtree.iter('edge')
for dump_edge in dump_edges:
	edge = next(edges)

	dump_speed = float(dump_edge.get('speed',-1.0))
	edge.set('dump_speed',str(dump_speed))

	#dump_traveltime = float(dump_edge.get('traveltime',-1.0))
	#edge.set('dump_traveltime',str(dump_traveltime))

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

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()
dump_file.close()
weights_node_file.close()
weights_edge_file.close()