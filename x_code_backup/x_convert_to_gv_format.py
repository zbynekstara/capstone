# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.nod.xml', 'r')
edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.edg.xml', 'r')

graphviz_file = open('C:\Users\zs633\Capstone\AUH\osm\output\graphviz.gv', 'w')
info_file = open('C:\Users\zs633\Capstone\AUH\osm\info\google.colors.txt', 'w')

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

# WRITE NODES AND EDGES IN GRAPHVIZ FORMAT
print "write nodes and edges in graphviz format"

# constants
graphviz_len_modifier = 1.0/15.0 # to get the scale of graphviz output in line with netedit output (?) # value for 0.01 min, 0.50 should have 1/(15.0*50)
graphviz_weight_modifier = 100.0 # to tweak weighting of springs (?)

min_edge_len_modifier = 0.01 * graphviz_len_modifier # nodes with weight 0 will get 1% of their length as desired edge length
max_edge_len_modifier = 1.00 * graphviz_len_modifier # nodes with weight 100 will get 100% of their length as desired edge length

gv_string = "digraph G {\n"

node_translation_dict = dict()
nodes = node_subtree.iter('node')
node_index = 0
for node in nodes: # list nodes with positions
	node_id = node.get('id')
	node_x = node.get('x')
	node_y = node.get('y')

	gv_string += "\t"+node_id+" [pos=\""+node_x+","+node_y+"\"];\n"

	node_index += 1

edges = edge_subtree.iter('edge')
for edge in edges:
	edge_from = edge.get('from')
	edge_to = edge.get('to')

	edge_len = float(edge.get('len'))

	slowdown_ratio = edge.get('slowdown_ratio')

	len_modifier = diff_speed_ratio # positive version
	#len_modifier = 1.0-diff_speed_ratio # negative version

	desired_edge_len = (min_edge_len_modifier*edge_len) + ((max_edge_len_modifier-min_edge_len_modifier)*edge_len*len_modifier)

	edge_weight = len_modifier * graphviz_weight_modifier

	gv_string += "\t"+modified_edge_from+" -> "+modified_edge_to+" [len=\""+str(desired_edge_len)+"\",weight=\""+str(edge_weight)+"\"];\n"

gv_string += "}"

print "prepare info file"
new_edges = new_edge_root.iter('edge')
# google colormap in terms of diff_speed_ratio: 0.00-0.23, 0.23-0.54, 0.54-0.92, 0.92-1.00
black_edges = 0
red_edges = 0
yellow_edges = 0
green_edges = 0
for new_edge in new_edges:
	slowdown = float(new_edge.get('diff_speed_ratio',0.0))
	if slowdown > 0.92:
		black_edges += 1
		continue
	if slowdown > 0.54:
		red_edges += 1
		continue
	if slowdown > 0.23:
		yellow_edges += 1
		continue
	# else
	green_edges += 1

info_string = ""
info_string += "black edges: "+str(black_edges)+"\n"
info_string += "red edges: "+str(red_edges)+"\n"
info_string += "yellow edges: "+str(yellow_edges)+"\n"
info_string += "green edges: "+str(green_edges)+"\n"

# WRITE OUTPUT FILES
print "write output files"
graphviz_file.write(gv_string)
info_file.write(info_string)

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()
dump_file.close()
graphviz_file.close()
info_file.close()