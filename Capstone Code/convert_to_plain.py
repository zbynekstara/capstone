# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

graphviz_file = open('F:\Capstone\AUH\osm\output\graphviz.out.gv', 'r') # F:\Capstone\AUH\osm\output\graphviz.out.gv

graphviz_node_file = open('F:\Capstone\AUH\osm\output\graphviz.nod.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.nod.xml
graphviz_edge_file = open('F:\Capstone\AUH\osm\output\graphviz.edg.xml', 'w') # F:\Capstone\AUH\osm\output\graphviz.edg.xml

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

gv_string = "graph G {\n"

nodes = node_subtree.iter('node')
for node in nodes:
	# list nodes with positions
	gv_string += "\t"+node.get('id').replace('-','##')+" [pos=\""+node.get('x')+","+node.get('y')+"\"];\n"

edges = edge_subtree.iter('edge')
for edge in edges:
	# list edge connections
	#if edge.get('to') is not None and edge.get('from') is not None:
	gv_string += "\t"+edge.get('from').replace('-','##')+" -- "+edge.get('to').replace('-','##')+" [id=\""+edge.get('id').replace('-','##')+"\",weight=\""+edge.get('weight')+"\"];\n"

gv_string += "}"

# WRITE OUTPUT FILES
print "write output files"
graphviz_edge_file.write(gv_string)

# CLOSE FILES
print "close files"
weights_node_file.close()
weights_edge_file.close()
graphviz_edge_file.close()