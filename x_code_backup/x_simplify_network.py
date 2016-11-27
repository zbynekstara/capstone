# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('C:\Users\zs633\Capstone\AUH\osm\plain\island.nod.xml', 'r')
edge_file = open('C:\Users\zs633\Capstone\AUH\osm\plain\island.edg.xml', 'r')
con_file =  open('C:\Users\zs633\Capstone\AUH\osm\plain\island.con.xml', 'r')
tll_file =  open('C:\Users\zs633\Capstone\AUH\osm\plain\island.tll.xml', 'r')

simplified_node_file = open('C:\Users\zs633\Capstone\AUH\osm\simplified\simplified.nod.xml', 'w')
simplified_edge_file = open('C:\Users\zs633\Capstone\AUH\osm\simplified\simplified.edg.xml', 'w')
simplified_con_file = open('C:\Users\zs633\Capstone\AUH\osm\simplified\simplified.con.xml', 'w')
simplified_tll_file = open('C:\Users\zs633\Capstone\AUH\osm\simplified\simplified.tll.xml', 'w')

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

# READ CONNECTION FILE TO GET CONNECTIONS
print "read con file"
con_tree = ET.parse(con_file)
con_root = con_tree.getroot()

file_cons = con_root.iter('connection')
con_subtree = ET.Element('con_subtree_root')
con_len = 0
for file_con in file_cons:
	con_subtree.append(file_con)
	con_len += 1
print str(con_len)

# READ TLL FILE TO GET TLLS (UNCHANGED)
print "read tll file"
tll_tree = ET.parse(tll_file)
tll_root = tll_tree.getroot()

file_tlls = tll_root.iter('tlLogic')
tll_subtree = ET.Element('tll_subtree_root')
tll_len = 0
for file_tll in file_tlls:
	tll_subtree.append(file_tll)
	tll_len += 1
print str(tll_len)

file_tll_cons = tll_root.iter('connection')
tll_con_subtree = ET.Element('tll_con_subtree_root')
tll_con_len = 0
for file_tll_con in file_tll_cons:
	tll_con_subtree.append(file_tll_con)
	tll_con_len += 1
print str(tll_con_len)

# FILTER
print "filter edges and nodes"

new_edge_root = ET.Element(edge_root.tag,attrib=edge_root.attrib)
new_edge_tree = ET.ElementTree(new_edge_root)
filtered_edge_len = 0

new_node_root = ET.Element(node_root.tag,attrib=node_root.attrib)
new_node_tree = ET.ElementTree(new_node_root)
filtered_node_len = 0

new_con_root = ET.Element(con_root.tag,attrib=con_root.attrib)
new_con_tree = ET.ElementTree(new_con_root)
filtered_con_len = 0

new_tll_root = ET.Element(tll_root.tag,attrib=tll_root.attrib)
new_tll_tree = ET.ElementTree(new_tll_root)
filtered_tll_len = 0

file_edges = edge_root.iter('edge')
for file_edge in file_edges:
	file_edge_speed = float(file_edge.get('speed',-1.0))
	if file_edge_speed > 15: # just above 50 kph, should only look at major roads
		new_edge_root.append(file_edge)
		filtered_edge_len += 1

		file_edge_from = file_edge.get('from', None)
		if file_edge_from is not None: # if edge has a from node
			if new_node_tree.find('node[@id=\''+file_edge_from+'\']') is None: # if the from node is not yet in new node tree
				new_node = node_tree.find('node[@id=\''+file_edge_from+'\']') # find it in node tree
				new_node_root.append(new_node) # add it to new node tree
				filtered_node_len += 1
				# TODO
		file_edge_to = file_edge.get('to', None)
		if file_edge_to is not None: # if edge has a to node
			if new_node_tree.find('node[@id=\''+file_edge_to+'\']') is None: # if the to node is not yet in new node tree
				new_node = node_tree.find('node[@id=\''+file_edge_to+'\']') # find it in node tree
				new_node_root.append(new_node) # add it to new node tree
				filtered_node_len += 1
				# TODO
print "filtered edge_len: "+str(filtered_edge_len)
print "filtered node len: "+str(filtered_node_len)

# WRITE OUTPUT FILES
print "write output files"
new_node_tree.write(simplified_node_file,encoding='UTF-8',xml_declaration=True)
new_edge_tree.write(simplified_edge_file,encoding='UTF-8',xml_declaration=True)

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()
con_file.close()
tll_file.close()
simplified_node_file.close()
simplified_edge_file.close()
simplified_con_file.close()
simplified_tll_file.close()