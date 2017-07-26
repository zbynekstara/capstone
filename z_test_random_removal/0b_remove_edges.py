# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET
import random

# OPEN FILES
print "open files"

edge_file = open('./0a_plain/test.edg.xml', 'r')

new_edge_file = open('./0b_modified/test.edg.xml', 'w')

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

# REMOVE EDGES
print "remove edges"
removal_probability = 0.15

print 'number of edges: ' + str(edge_len)

number_to_remove = int(float(edge_len) * (removal_probability))
if number_to_remove % 2 == 1:
	if removal_probability > 0.5:
		number_to_remove -= 1
	else:
		number_to_remove += 1
print 'number to remove: ' + str(number_to_remove)

removed = 0

#edges = list(edge_subtree.iter('edge'))
while removed < number_to_remove:
	edge = random.choice(list(edge_subtree.iter('edge')))
	# remove this edge and its mirror

	edge_from = edge.get('from')
	edge_to = edge.get('to')

	edge_mirror = edge_subtree.find('edge[@from=\''+str(edge_to)+'\'][@to=\''+str(edge_from)+'\']')

	print 'removing: ' + str(edge.get('id')) + ' ' + str(edge_mirror.get('id'))
	edge_subtree.remove(edge)
	edge_subtree.remove(edge_mirror)

	removed += 2
print 'removed: ' + str(removed)

new_edge_root = ET.Element(edge_root.tag,attrib=edge_root.attrib)
new_edge_tree = ET.ElementTree(new_edge_root)
new_edge_root.extend(edge_subtree)

edge_len = len(list(new_edge_root.iter('edge')))
print 'new number of edges: ' + str(edge_len)
# WRITE OUTPUT FILES
print "write output files"
new_edge_tree.write(new_edge_file,encoding='UTF-8',xml_declaration=True)

# CLOSE FILES
print "close files"
edge_file.close()
new_edge_file.close()