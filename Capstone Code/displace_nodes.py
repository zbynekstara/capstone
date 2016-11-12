# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.nod.xml', 'r')
edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\modified.edg.xml', 'r')

lensing_node_file = open('C:\Users\zs633\Capstone\AUH\osm\output\lensing.nod.xml', 'w')
lensing_edge_file = open('C:\Users\zs633\Capstone\AUH\osm\output\lensing.edg.xml', 'w')

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

# CONSTRCT TRANSLATION DICTIONARY
print "construct translation dictionary"
lensing_translation_dict = dict()
c = 0.0 # q/r

# first part, calculating a based on c while lensing is possible
current_a = 0.0000
sum_c = 0.00000
num_c = 0.0
while ((c/math.sqrt(1.0-math.pow(c,2)))+c) < 1.00000:
	a = c/math.sqrt(1.0-math.pow(c,2))

	if round(a,4) != current_a: # reset for new numbers
		current_a = round(a,4)
		sum_c = 0.00000
		num_c = 0

	sum_c += c
	num_c += 1.0

	#print "a="+str(current_a)+" c="+str(sum_c/num_c)
	lensing_translation_dict[str(current_a)] = round(sum_c/num_c,4)
	
	#b = a + c # y/r
	c += 0.00001

# second part, continuing so that b would be 1 for everything
# this is because of the total internal reflection phenomenon
current_a += 0.0001
while current_a <= 1.0000:
	c = round((1.0000-current_a),4)

	#print "a="+str(current_a)+" c="+str(c)
	lensing_translation_dict[str(current_a)] = c

	current_a += 0.0001

#print lensing_translation_dict

# DESIGNATE FIXED NODES
print "designate fixed nodes"
nodes = node_subtree.iter('node')
num_junctions = 0
for node in nodes:
	node_weight_num = float(node.get('weight_num',0.0))
	if node_weight_num > 1.0:
		node.set('junction','True')
		num_junctions += 1

fixed_cutoff = int(0.25 * float(num_junctions)) # CONSTANT
nodes = node_subtree.iter('node')
counter = 0
for node in nodes:
	if counter > fixed_cutoff:
		break

	is_junction = bool(node.get('junction',False))
	if is_junction:
		node.set('fixed','True')

	counter += 1

# DISPLACE NODES BASED ON THE LENSING EFFECT OF MOST CONGESTED NODES
print "displace nodes"
max_radius = 350.0 # CONSTANT # max raindrop radius in meters - for 100% congested junction

nodes = node_subtree.iter('node')
counter = 0
for node in nodes:
	print str(counter)
	is_junction = bool(node.get('junction',False))

	if is_junction:
		node_weight = float(node.get('avg_slowdown_ratio', 0.0))
		radius = max_radius * node_weight # raindrop radius

		this_x = float(node.get('x'))
		this_y = float(node.get('y'))

		other_nodes = node_subtree.iter('node')
		for other_node in other_nodes:
			is_fixed = bool(node.get('fixed',False))
			if not is_fixed:
				other_x = float(other_node.get('x'))
				other_y = float(other_node.get('y'))

				nodes_distance = math.hypot(abs(other_x-this_x),abs(other_y-this_y)) # x
				if nodes_distance > 0.0 and nodes_distance < radius:
					a = round(nodes_distance/radius,4)
					c = lensing_translation_dict[str(a)]

					multiplier = c/a
					other_x_displacement = multiplier * (other_x-this_x)
					other_y_displacement = multiplier * (other_y-this_y)

					other_x_displacement_sum = float(other_node.get('x_displacement_sum',0.0))
					other_y_displacement_sum = float(other_node.get('y_displacement_sum',0.0))

					other_node.set('x_displacement_sum',str(other_x_displacement_sum+other_x_displacement))
					other_node.set('y_displacement_sum',str(other_y_displacement_sum+other_y_displacement))

					"""other_x_displacement_num = float(other_node.get('x_displacement_num',0.0)) # incremented if doesn't exist (so zero is okay)
					other_y_displacement_num = float(other_node.get('y_displacement_num',0.0))

					other_node.set('x_displacement_num',str(other_x_displacement_num+1.0))
					other_node.set('y_displacement_num',str(other_y_displacement_num+1.0))"""

	counter += 1

nodes = node_subtree.iter('node')
for node in nodes:
	old_x = float(node.get('x'))
	old_y = float(node.get('y'))

	node.set('old_x',str(old_x))
	node.set('old_y',str(old_y))

	x_displacement_sum = float(node.get('x_displacement_sum',0.0))
	y_displacement_sum = float(node.get('y_displacement_sum',0.0))

	"""x_displacement_num = float(node.get('x_displacement_num',1.0)) # to avoid division by zero
	y_displacement_num = float(node.get('y_displacement_num',1.0))"""

	new_x = old_x + x_displacement_sum#(x_displacement_sum/x_displacement_num) # add the average of displacements
	new_y = old_y + y_displacement_sum#(y_displacement_sum/y_displacement_num)

	node.set('x',str(new_x))
	node.set('y',str(new_y))

# WRITE OUTPUT FILES
print "write output files"
node_tree.write(lensing_node_file,encoding='UTF-8',xml_declaration=True)
edge_tree.write(lensing_edge_file,encoding='UTF-8',xml_declaration=True)

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()
lensing_node_file.close()
lensing_edge_file.close()