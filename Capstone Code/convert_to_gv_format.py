# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

weights_node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\weights.nod.xml', 'r') # sys.argv[1] F:\Capstone\AUH\osm\output\weights.nod.xml
weights_edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\weights.edg.xml', 'r') # sys.argv[1] F:\Capstone\AUH\osm\output\weights.edg.xml
dump_file = open('C:\Users\zs633\Capstone\AUH\osm\duarouter\island.dump.xml', 'r') # sys.argv[3] F:\Capstone\AUH\osm\duarouter\island.dump.xml

modified_node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.nod.xml', 'w') # F:\Capstone\AUH\osm\output\modified.nod.xml
modified_edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.edg.xml', 'w') # F:\Capstone\AUH\osm\output\modified.edg.xml
modified_dump_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.dump.xml', 'w') # F:\Capstone\AUH\osm\output\modified.dump.xml
graphviz_file = open('C:\Users\zs633\Capstone\AUH\osm\output\graphviz.gv', 'w') # F:\Capstone\AUH\osm\output\graphviz.gv
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

# READ DUMP FILE TO WRITE DOWN ADDITIONAL DATA
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

# WRITE NODES AND EDGES IN GRAPHVIZ FORMAT
print "write nodes and edges in graphviz format and creating modified dump file"

# constants
graphviz_len_modifier = 1.0/15.0 # to get the scale of graphviz output in line with netedit output (?) # value for 0.01 min, 0.50 should have 1/(15.0*50)
graphviz_weight_modifier = 100.0 # to tweak weighting of springs (?)

min_edge_len_modifier = 1.00 * graphviz_len_modifier # nodes with weight 0 will get 1% of their length as desired edge length
max_edge_len_modifier = 1.00 * graphviz_len_modifier # nodes with weight 100 will get 100% of their length as desired edge length

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

dump_edges = dump_edge_subtree.iter('edge')
edges = edge_subtree.iter('edge')
for edge in edges:
	# list edge connections
	edge_from = edge.get('from')
	edge_to = edge.get('to')

	#edge_id = edge.get('id')
	#dump_edge = dump_edge_subtree.find('edge[@id=\''+edge_id+'\']') # if this is too slow, make into iterator - order matches edge order
	dump_edge = next(dump_edges) # the order of dump edges perfectly matches the order of edges

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

	# LOOK INTO THE SPRING COEFFICEINT FOR NEATO!!!!!

	#desired length should be traveltime
	#weight should be real_speed = edgelen/traveltime #OR inverse of traveltime = 1/traveltime
	free_speed = float(edge.get('speed')) # free flow speed
	dump_edge.set('free_speed',str(free_speed))

	dump_speed = float(edge.get('dump_speed')) # speed with traffic
	if dump_speed == 0.00:
		# dump speed can be 0.00 - was not enough to be rounded to 0.01 but was not 0 either
		dump_speed = 0.004999
		# this produces problems when the graph is being generated
		# need to have a metric that takes the original length into account to preserve shapes
	if dump_speed == -1.0:
		# nodes that had no cars at all
		dump_speed = free_speed

	diff_speed = free_speed - dump_speed
	#edge.set('diff_speed',str(diff_speed))
	dump_edge.set('diff_speed',str(diff_speed))

	diff_speed_ratio = diff_speed / free_speed # how much slower is traffic than it should be? 1 = same speed as free flow, 0 = no movement
	dump_edge.set('diff_speed_ratio', str(diff_speed_ratio))

	#traveltime = edge_len / speed
	#desired_edge_len = traveltime

	# negative_edge_weight = dump_speed/free_flow_speed
	#negative_edge_weight = 100.0-negative_edge_weight
	desired_edge_len = (min_edge_len_modifier*edge_len) + ((max_edge_len_modifier-min_edge_len_modifier)*edge_len*diff_speed_ratio)

	edge_weight = diff_speed_ratio * graphviz_weight_modifier

	gv_string += "\t"+modified_edge_from+" -> "+modified_edge_to+" [len=\""+str(desired_edge_len)+"\",weight=\""+str(edge_weight)+"\"];\n"

gv_string += "}"
#neg_string += "}"

# WRITE OUTPUT FILES
print "write output files"
node_tree.write(modified_node_file,encoding='UTF-8',xml_declaration=True)
edge_tree.write(modified_edge_file,encoding='UTF-8',xml_declaration=True)
dump_tree.write(modified_dump_file,encoding='UTF-8',xml_declaration=True)
graphviz_file.write(gv_string)
#graphviz_positive_file.write(pos_string)
#graphviz_negative_file.write(neg_string)

# CLOSE FILES
print "close files"
weights_node_file.close()
weights_edge_file.close()
dump_file.close()
modified_node_file.close()
modified_edge_file.close()
modified_dump_file.close()
graphviz_file.close()
#graphviz_positive_file.close()
#graphviz_negative_file.close()