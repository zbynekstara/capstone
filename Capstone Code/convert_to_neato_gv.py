# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

weights_node_file = open('F:\Capstone\AUH\osm\output\weights.nod.xml', 'r') # sys.argv[1] F:\Capstone\AUH\osm\output\weights.nod.xml
weights_edge_file = open('F:\Capstone\AUH\osm\output\weights.edg.xml', 'r') # sys.argv[1] F:\Capstone\AUH\osm\output\weights.edg.xml

modified_node_file = open('F:\Capstone\AUH\osm\output\modified.nod.xml', 'w') # F:\Capstone\AUH\osm\output\modified.nod.xml
modified_edge_file = open('F:\Capstone\AUH\osm\output\modified.edg.xml', 'w') # F:\Capstone\AUH\osm\output\modified.edg.xml
graphviz_file = open('F:\Capstone\AUH\osm\output\graphviz.gv', 'w') # F:\Capstone\AUH\osm\output\graphviz.gv
#graphviz_positive_file = open('F:\Capstone\AUH\osm\output\graphviz.pos.gv', 'w') # F:\Capstone\AUH\osm\output\graphviz.pos.gv
#graphviz_negative_file = open('F:\Capstone\AUH\osm\output\graphviz.neg.gv', 'w') # F:\Capstone\AUH\osm\output\graphviz.neg.gv

# READ NODE FILE TO GET NODES
print "read node file"
node_tree = ET.parse(weights_node_file)
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
edge_tree = ET.parse(weights_edge_file)
edge_root = edge_tree.getroot()

file_edges = edge_root.iter('edge')
edge_subtree = ET.Element('edge_subtree_root')
edge_len = 0
for file_edge in file_edges:
	edge_subtree.append(file_edge)
	edge_len += 1
print str(edge_len)

# WRITE NODES AND EDGES IN GRAPHVIZ FORMAT
print "write nodes and edges in graphviz format"

# constants
#min_edge_len_modifier = 0.01 # nodes with weight 0 will get 1% of their length as desired edge length (positive - negative give 1% desired to 100-weighted nodes)
#max_edge_len_modifier = 1.00 # nodes with weight 100 will get 100% of their length as desired edge length (positive - negative gives 100% desired to 0-weighted nodes)

gv_string = "digraph G {\n"
#neg_string = "digraph G {\n"

node_translation_dict = dict()
nodes = node_subtree.iter('node')
node_index = 0
for node in nodes:
	# list nodes with positions
	node_id = node.get('id')
	node_x = node.get('x')
	node_y = node.get('y')

	#modified_node_id = "node_"+node_id.replace('-','a_dash_a').replace('#','a_hash_a')
	# renaming nodes with numbers based on order listed
	node_translation_dict[node_id] = str(node_index)
	modified_node_id = "node_"+str(node_index)

	node.set('id',modified_node_id)

	gv_string += "\t"+modified_node_id+" [pos=\""+node_x+","+node_y+"\"];\n"
	#neg_string += "\t"+modified_node_id+" [pos=\""+node_x+","+node_y+"\"];\n"

	node_index += 1

edges = edge_subtree.iter('edge')
for edge in edges:
	# list edge connections
	edge_from = edge.get('from')
	edge_to = edge.get('to')
	#edge_id = edge.get('id')

	#modified_edge_from = "node_"+edge_from.replace('-','a_dash_a').replace('#','a_hash_a')
	#modified_edge_to = "node_"+edge_to.replace('-','a_dash_a').replace('#','a_hash_a')
	#modified_edge_id = "edge_"+edge_id.replace('-','a_dash_a').replace('#','a_hash_a')
	# using renamed node names
	modified_edge_from = "node_"+node_translation_dict[edge_from]
	modified_edge_to = "node_"+node_translation_dict[edge_to]

	edge.set('from',modified_edge_from)
	edge.set('to',modified_edge_to)

	node_from = node_subtree.find('node[@id=\''+modified_edge_from+'\']') # assumes that the node is present in node list
	node_from_x = float(node_from.get('x'))
	node_from_y = float(node_from.get('y'))
	node_to = node_subtree.find('node[@id=\''+modified_edge_to+'\']') # assumes that the node is present in node list
	node_to_x = float(node_to.get('x'))
	node_to_y = float(node_to.get('y'))
	edge_len = math.hypot(abs(node_from_x-node_to_x),abs(node_from_y-node_to_y)) # hypotenuse

	#positive_edge_weight = float(edge.get('weight'))
	#negative_edge_weight = 100.0-positive_edge_weight
	#desired_positive_edge_len = (min_edge_len_modifier*edge_len) + ((max_edge_len_modifier-min_edge_len_modifier)*edge_len*(positive_edge_weight/100.0))

	#desired length should be traveltime
	#weight should be real_speed = edgelen/traveltime #OR inverse of traveltime = 1/traveltime
	speed = float(edge.get('dump_speed'))
	if speed == -1.0:
		# nodes that had no cars at all
		speed = float(edge.get('speed'))

	traveltime = edge_len/speed
	
	desired_edge_len = traveltime
	edge_weight = speed

	gv_string += "\t"+modified_edge_from+" -> "+modified_edge_to+" [len=\""+str(desired_edge_len)+"\",weight=\""+str(edge_weight)+"\"];\n"
	#neg_string += "\t"+modified_edge_from+" -> "+modified_edge_to+" [len=\""+str(desired_negative_edge_len)+"\",weight=\""+str(negative_edge_weight)+"\"];\n"

gv_string += "}"
#neg_string += "}"

# WRITE OUTPUT FILES
print "write output files"
node_tree.write(modified_node_file,encoding='UTF-8',xml_declaration=True)
edge_tree.write(modified_edge_file,encoding='UTF-8',xml_declaration=True)
graphviz_file.write(gv_string)
#graphviz_positive_file.write(pos_string)
#graphviz_negative_file.write(neg_string)

# CLOSE FILES
print "close files"
weights_node_file.close()
weights_edge_file.close()
modified_node_file.close()
modified_edge_file.close()
graphviz_file.close()
#graphviz_positive_file.close()
#graphviz_negative_file.close()