# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

weights_node_file = open('./5_weights/weights.nod.xml', 'r')
weights_edge_file = open('./5_weights/weights.edg.xml', 'r')
weights_dump_file = open('./5_weights/weights.dump.xml', 'r')

modified_node_file = open('./6_prepared/modified.nod.xml', 'w')
modified_edge_file = open('./6_prepared/modified.edg.xml', 'w')
modified_dump_file = open('./6_prepared/modified.dump.xml', 'w')

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

# READ DUMP FILE
print "read dump file"
dump_edge_tree = ET.parse(weights_dump_file)
dump_edge_root = dump_edge_tree.getroot().find('interval')

file_dump_edges = dump_edge_root.iter('edge')
dump_edge_subtree = ET.Element('dump_edge_subtree_root')
dump_edge_len = 0
for file_dump_edge in file_dump_edges:
	dump_edge_subtree.append(file_dump_edge)
	dump_edge_len += 1
print str(dump_edge_len)

"""# CREATE MODIFIED NODE FILE
print "create modified node file"
node_translation_dict = dict()
nodes = node_subtree.iter('node')
node_index = 0
for node in nodes:
	node_id = node.get('id')

	# renaming nodes with numbers based on order listed
	node_translation_dict[node_id] = str(node_index)
	modified_node_id = "node_"+str(node_index)

	node.set('id',modified_node_id)

	node_index += 1

# CREATE MODIFIED EDGE FILE
print "create modified edge file"
edge_translation_dict = dict()
edges = edge_subtree.iter('edge')
dump_edges = dump_edge_subtree.iter('edge')
edge_index = 0
for edge in edges:
	dump_edge = next(dump_edges) # the order of dump edges perfectly matches the order of edges

	edge_id = edge.get('id')

	# renaming edges with numbers based on order listed
	edge_translation_dict[edge_id] = str(edge_index)
	modified_edge_id = "edge_"+str(edge_index)

	edge.set('id',modified_edge_id)
	dump_edge.set('id',modified_edge_id)

	# list edge connections
	edge_from = edge.get('from')
	edge_to = edge.get('to')

	# using renamed node names
	modified_edge_from = "node_"+node_translation_dict[edge_from]
	modified_edge_to = "node_"+node_translation_dict[edge_to]

	edge.set('from',modified_edge_from)
	edge.set('to',modified_edge_to)

	edge_index += 1"""

# SORT MODIFIED NODE TREE
print "sort modified node tree"
new_node_root = ET.Element(node_root.tag,attrib=edge_root.attrib)
new_node_tree = ET.ElementTree(new_node_root)

def getkey(elem):
	return float(elem.get('avg_slowdown_ratio',0.0))
new_node_subtree = sorted(node_subtree,key=getkey,reverse=True)

new_node_root.extend(new_node_subtree)

# SORT MODIFIED EDGE TREE
print "sort modified edge tree"
new_edge_root = ET.Element(edge_root.tag,attrib=edge_root.attrib)
new_edge_tree = ET.ElementTree(new_edge_root)

new_dump_edge_root = ET.Element(dump_edge_root.tag,attrib=dump_edge_root.attrib)
new_dump_edge_tree = ET.ElementTree(new_dump_edge_root)

def getkey(elem):
	return float(elem.get('slowdown_ratio',0.0))
new_edge_subtree = sorted(edge_subtree,key=getkey,reverse=True)
new_dump_edge_subtree = sorted(dump_edge_subtree,key=getkey,reverse=True)

new_edge_root.extend(new_edge_subtree)
new_dump_edge_root.extend(new_dump_edge_subtree)

# WRITE OUTPUT FILES
print "write output files"
new_node_tree.write(modified_node_file,encoding='UTF-8',xml_declaration=True)
new_edge_tree.write(modified_edge_file,encoding='UTF-8',xml_declaration=True)
new_dump_edge_tree.write(modified_dump_file,encoding='UTF-8',xml_declaration=True)

# CLOSE FILES
print "close files"
weights_node_file.close()
weights_edge_file.close()
weights_dump_file.close()
modified_node_file.close()
modified_edge_file.close()
modified_dump_file.close()