# -*- coding: utf-8 -*-

import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('./6_prepared/modified.nod.xml', 'r')
edge_file = open('./6_prepared/modified.edg.xml', 'r')

gravity_node_file = open('./7_displaced/linear.nod.xml', 'w')
gravity_edge_file = open('./7_displaced/linear.edg.xml', 'w')
info_file = open('./10d_info/stats.google.txt', 'w')

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

# DESIGNATE FIXED NODES
print "designate fixed nodes"
edges = edge_subtree.iter('edge')
for edge in edges:
	edge_speed = float(edge.get('speed'))
	if edge_speed > 15:
		# 15 mps = 50 kph/30 mph
		# 18 mps = 60 kph/40 mph
		edge_from = edge.get('from')
		edge_to = edge.get('to')

		node_from = node_subtree.find('node[@id=\''+edge_from+'\']')
		node_from.set('fixed','True')

		node_to = node_subtree.find('node[@id=\''+edge_to+'\']')
		node_to.set('fixed','True')

# DESIGNATE JUNCTIONS
print "designate junctions"
nodes = node_subtree.iter('node')
#num_junctions = 0
for node in nodes:
	node_weight_num = float(node.get('weight_num',0.0))
	if node_weight_num > 1.0:
		node.set('junction','True')
		#num_junctions += 1

# DISPLACE NODES
print "displace nodes"
max_radius = 333.0
fixed_modifier = 0.1

nodes = node_subtree.iter('node')
counter = 0
for node in nodes:
	print str(counter)
	is_junction = bool(node.get('junction',False))

	if is_junction: # if this node can move things
		node_weight = float(node.get('avg_slowdown_ratio', 0.0))
		radius = max_radius * node_weight

		this_x = float(node.get('x'))
		this_y = float(node.get('y'))

		other_nodes = node_subtree.iter('node')
		for other_node in other_nodes:
			is_fixed = bool(other_node.get('fixed',False))

			other_x = float(other_node.get('x'))
			other_y = float(other_node.get('y'))

			nodes_distance = math.hypot(abs(other_x-this_x),abs(other_y-this_y))
			if nodes_distance > 0.0 and radius > 0.0 and nodes_distance <= radius: # must not be zero
				old_dist = nodes_distance # x

				new_dist = ((math.pow(radius,2.0)-math.sqrt(4.0*math.pow(radius,3.0)*old_dist-3.0*math.pow(radius,2.0)*math.pow(old_dist,2.0))+radius*old_dist-math.pow(old_dist,2.0))/(math.pow(radius,2.0)+math.pow(old_dist,2.0)))*old_dist # x'-x = displacememnt
				
				multiplier = new_dist/old_dist
				if is_fixed: # this node should not move as much as it normally would
					multiplier *= fixed_modifier
				
				other_x_displacement = multiplier * (other_x-this_x)
				other_y_displacement = multiplier * (other_y-this_y)

				other_x_displacement_sum = float(other_node.get('x_displacement_sum',0.0))
				other_y_displacement_sum = float(other_node.get('y_displacement_sum',0.0))

				other_node.set('x_displacement_sum',str(other_x_displacement_sum+other_x_displacement))
				other_node.set('y_displacement_sum',str(other_y_displacement_sum+other_y_displacement))

	counter += 1

nodes = node_subtree.iter('node')
for node in nodes:
	old_x = float(node.get('x'))
	old_y = float(node.get('y'))

	node.set('old_x',str(old_x))
	node.set('old_y',str(old_y))

	x_displacement_sum = float(node.get('x_displacement_sum',0.0))
	y_displacement_sum = float(node.get('y_displacement_sum',0.0))

	new_x = old_x + x_displacement_sum
	new_y = old_y + y_displacement_sum

	node.set('x',str(new_x))
	node.set('y',str(new_y))

# REMOVE EDGE SHAPES
print "remove edge shapes"
edges = edge_subtree.iter('edge')
for edge in edges:
	edge.attrib.pop('shape',None) # get rid of the shape attribute

# PREPARE INFO FILE FOR GOOGLE COLORS
print "prepare info file"
edges = edge_root.iter('edge')
# google colormap in terms of slowdown_ratio: 0.00-0.23, 0.23-0.54, 0.54-0.92, 0.92-1.00
black_edges = 0
red_edges = 0
yellow_edges = 0
green_edges = 0
for edge in edges:
	slowdown_ratio = float(edge.get('slowdown_ratio',0.0))
	if slowdown_ratio > 0.92:
		black_edges += 1
		continue
	if slowdown_ratio > 0.54:
		red_edges += 1
		continue
	if slowdown_ratio > 0.23:
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
node_tree.write(gravity_node_file,encoding='UTF-8',xml_declaration=True)
edge_tree.write(gravity_edge_file,encoding='UTF-8',xml_declaration=True)
info_file.write(info_string)

# CLOSE FILES
print "close files"
node_file.close()
edge_file.close()
gravity_node_file.close()
gravity_edge_file.close()
info_file.close()