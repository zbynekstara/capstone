# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.nod.xml', 'r') # F:\Capstone\AUH\osm\output\modified.nod.xml
#positive_node_file = open('F:\Capstone\AUH\osm\output\modified.nod.xml', 'r') # F:\Capstone\AUH\osm\output\modified.nod.xml
#negative_node_file = open('F:\Capstone\AUH\osm\output\modified.nod.xml', 'r') # F:\Capstone\AUH\osm\output\modified.nod.xml
edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.edg.xml', 'r') # F:\Capstone\AUH\osm\output\modified.edg.xml
con_file =  open('C:\Users\zs633\Capstone\AUH\osm\plain\island.con.xml', 'r') # F:\Capstone\AUH\osm\plain\island.con.xml
tll_file =  open('C:\Users\zs633\Capstone\AUH\osm\plain\island.tll.xml', 'r') # F:\Capstone\AUH\osm\plain\island.tll.xml
graphviz_file = open('C:\Users\zs633\Capstone\AUH\osm\output\graphviz.out.gv', 'r') # F:\Capstone\AUH\osm\output\graphviz.out.gv
#graphviz_positive_file = open('F:\Capstone\AUH\osm\output\graphviz.pos.out.gv', 'r') # F:\Capstone\AUH\osm\output\graphviz.pos.out.gv
#graphviz_negative_file = open('F:\Capstone\AUH\osm\output\graphviz.neg.out.gv', 'r') # F:\Capstone\AUH\osm\output\graphviz.neg.out.gv

graphviz_node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\graphviz.nod.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.nod.xml
#graphviz_positive_node_file = open('F:\Capstone\AUH\osm\output\graphviz.pos.nod.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.pos.nod.xml
#graphviz_negative_node_file = open('F:\Capstone\AUH\osm\output\graphviz.neg.nod.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.neg.nod.xml
graphviz_edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\graphviz.edg.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.edg.xml
graphviz_con_file = open('C:\Users\zs633\Capstone\AUH\osm\output\graphviz.con.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.con.xml
graphviz_tll_file = open('C:\Users\zs633\Capstone\AUH\osm\output\graphviz.tll.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.tll.xml

# READ NODE FILE TO GET NODES
print "read node files"
node_tree = ET.parse(node_file)
node_root = node_tree.getroot()

file_nodes = node_root.iter('node')
node_subtree = ET.Element('node_subtree_root')
node_len = 0
for file_node in file_nodes:
	node_subtree.append(file_node)
	node_len += 1
print str(node_len)

"""positive_node_tree = ET.parse(positive_node_file)
positive_node_root = positive_node_tree.getroot()

positive_file_nodes = positive_node_root.iter('node')
positive_node_subtree = ET.Element('node_subtree_root')
positive_node_len = 0
for positive_file_node in positive_file_nodes:
	positive_node_subtree.append(positive_file_node)
	positive_node_len += 1
print str(positive_node_len)

negative_node_tree = ET.parse(negative_node_file)
negative_node_root = negative_node_tree.getroot()

negative_file_nodes = negative_node_root.iter('node')
negative_node_subtree = ET.Element('node_subtree_root')
negative_node_len = 0
for negative_file_node in negative_file_nodes:
	negative_node_subtree.append(negative_file_node)
	negative_node_len += 1
print str(negative_node_len)"""

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

# READ CONNECTION FILE TO GET CONNECTIONS (UNCHANGED)
print "read con file"
con_tree = ET.parse(con_file)
#con_root = con_tree.getroot()

# READ TLL FILE TO GET TLLS (UNCHANGED)
print "read tll file"
tll_tree = ET.parse(tll_file)
#tll_root = tll_tree.getroot().find('connection')

# READ GRAPHVIZ OUTPUT FILES
print "read graphviz output files"
graphviz_nodes = []
#bb = None
file_string = graphviz_file.read()
file_string = file_string.replace('\n\t\t','')
file_lines = file_string.split('\n')
for line in file_lines:
	if line.startswith('\tnode_'):
		line = line[1:]
		line = line.replace(' -> ','\t->\t').replace('\t ','\t').replace(';','')
		line_segments = line.split('\t')
		if line_segments[1] != '->':
			# this is a node definition
			node_id = line_segments[0]
			node_attributes = line_segments[1].split('\"')
			node_xy = node_attributes[1].split(',')
			node_position = (float(node_xy[0]),float(node_xy[1]))
			graphviz_nodes.append((node_id,node_position))
		else:
			# this is an edge definition
			# throw this line away
			pass
	elif line.startswith('\tgraph '):
		line = line[7:]
		line = line.replace(';','')
		bb_segments = line.split('\"')[1].split(',')
		bb = (float(bb_segments[0]),float(bb_segments[1]),float(bb_segments[2]),float(bb_segments[3]))
	else: # line does not start with \tnode_ # 3 initial lines and end line
		# throw this line away
		pass
# print graphviz_nodes

"""graphviz_positive_nodes = []
#positive_bb = None
positive_file_string = graphviz_positive_file.read()
positive_file_string = positive_file_string.replace('\n\t\t','')
positive_file_lines = positive_file_string.split('\n')
for positive_line in positive_file_lines:
	if positive_line.startswith('\tnode_'):
		positive_line = positive_line[1:]
		positive_line = positive_line.replace(' -> ','\t->\t').replace('\t ','\t').replace(';','')
		positive_line_segments = positive_line.split('\t')
		if positive_line_segments[1] != '->':
			# this is a node definition
			node_id = positive_line_segments[0]
			node_attributes = positive_line_segments[1].split('\"')
			node_xy = node_attributes[1].split(',')
			node_position = (float(node_xy[0]),float(node_xy[1]))
			graphviz_positive_nodes.append((node_id,node_position))
		else:
			# this is an edge definition
			# throw this line away
			pass
	#elif positive_line.startswith('\tgraph '):
		#positive_line = positive_line[7:]
		#positive_line = positive_line.replace(';','')
		#positive_bb_segments = positive_line.split('\"')[1]
		#positive_bb = (float(positive_bb_segments[0]),float(positive_bb_segments[1]),float(positive_bb_segments[2]),float(positive_bb_segments[3]))
	else: # line does not start with \tnode_ # 3 initial lines and end line
		# throw this line away
		pass
#print positive_nodes

graphviz_negative_nodes = []
#negative_bb = None
negative_file_string = graphviz_negative_file.read()
negative_file_string = negative_file_string.replace('\n\t\t','')
negative_file_lines = negative_file_string.split('\n')
for negative_line in negative_file_lines:
	if negative_line.startswith('\tnode_'):
		negative_line = negative_line[1:]
		negative_line = negative_line.replace(' -> ','\t->\t').replace('\t ','\t').replace(';','')
		negative_line_segments = negative_line.split('\t')
		if negative_line_segments[1] != '->':
			# this is a node definition
			node_id = negative_line_segments[0]
			node_attributes = negative_line_segments[1].split('\"')
			node_xy = node_attributes[1].split(',')
			node_position = (float(node_xy[0]),float(node_xy[1]))
			graphviz_negative_nodes.append((node_id,node_position))
		else:
			# this is an edge definition
			# throw this line away
			pass
	#elif negative_line.startswith('\tgraph '):
		#negative_line = negative_line[7:]
		#negative_line = negative_line.replace(';','')
		#negative_bb_segments = negative_line.split('\"')[1]
		#negative_bb = (float(negative_bb_segments[0]),float(negative_bb_segments[1]),float(negative_bb_segments[2]),float(negative_bb_segments[3]))
	else: # line does not start with \tnode_ # 3 initial lines and end line
		# throw this line away
		pass
#print negative_nodes"""

# APPLY NEW NODE POSITIONS
# nodes without new positions in previous version:
# cluster_3725030019_3725030020_cluster_2345185492_2345185566_2345185605_261615099_261615100_261615131_261615132_3725030017_3725030018_3725030021_3725030022_3725030023_4086616178_4086939207_4086939208_4087182092_4090156550
# cluster_262189146_262189159_262189160_2794578711_2794578716_4015846918_4015846919_4015846922_4015846923_4015846926_4201521855_4201521857_4201521859_4280981630_4314906425_4314906427
print "apply new node positions"

# constants
#netedit_bb = (0.00,0.00,18651.48,14880.02)

for graphviz_node in graphviz_nodes:
	original_node = node_subtree.find('node[@id=\''+graphviz_node[0]+'\']')
	original_node.set('x',str(graphviz_node[1][0]))
	original_node.set('y',str(graphviz_node[1][1]))

	#original_node.set('x',str( (graphviz_node[1][0] - bb[0])/(bb[2]-bb[0]) )

"""for graphviz_positive_node in graphviz_positive_nodes:
	original_node = positive_node_subtree.find('node[@id=\''+graphviz_positive_node[0]+'\']')
	original_node.set('x',str(graphviz_positive_node[1][0]))
	original_node.set('y',str(graphviz_positive_node[1][1]))

	#original_node.set('x',str( (graphviz_positive_node[1][0] - positive_bb[0])/(positive_bb[2]-positive_bb[0]) )

for graphviz_negative_node in graphviz_negative_nodes:
	original_node = negative_node_subtree.find('node[@id=\''+graphviz_negative_node[0]+'\']')
	original_node.set('x',str(graphviz_negative_node[1][0]))
	original_node.set('y',str(graphviz_negative_node[1][1]))"""

# ERASE EDGE SHAPES
print "erase edge shape data"
edges = edge_subtree.iter('edge')
for edge in edges:
	edge.attrib.pop('shape',None) # get rid of the shape attribute

# WRITE OUTPUT FILES
print "write output files"
node_tree.write(graphviz_node_file,encoding='UTF-8',xml_declaration=True)
#positive_node_tree.write(graphviz_positive_node_file,encoding='UTF-8',xml_declaration=True)
#negative_node_tree.write(graphviz_negative_node_file,encoding='UTF-8',xml_declaration=True)
edge_tree.write(graphviz_edge_file,encoding='UTF-8',xml_declaration=True)
con_tree.write(graphviz_con_file,encoding='UTF-8',xml_declaration=True)
tll_tree.write(graphviz_tll_file,encoding='UTF-8',xml_declaration=True)

# CLOSE FILES
print "close files"
node_file.close()
#positive_node_file.close()
#negative_node_file.close()
edge_file.close()
con_file.close()
tll_file.close()
graphviz_file.close()
#graphviz_positive_file.close()
#graphviz_negative_file.close()
graphviz_node_file.close()
#graphviz_positive_node_file.close()
#graphviz_negative_node_file.close()
graphviz_edge_file.close()
graphviz_con_file.close()
graphviz_tll_file.close()