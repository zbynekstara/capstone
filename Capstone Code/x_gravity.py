# -*- coding: utf-8 -*-

import sys
import math
import xml.etree.ElementTree as ET

# OPEN FILES
print "open files"

node_file = open('F:\Capstone\AUH\osm\plain\island.nod.xml', 'r') # sys.argv[1] F:\Capstone\AUH\osm\plain\island.nod.xml
edge_file = open('F:\Capstone\AUH\osm\plain\island.edg.xml', 'r') # sys.argv[2] F:\Capstone\AUH\osm\plain\island.edg.xml
con_file =  open('F:\Capstone\AUH\osm\plain\island.con.xml', 'r') # sys.argv[3] F:\Capstone\AUH\osm\plain\island.con.xml
tll_file =  open('F:\Capstone\AUH\osm\plain\island.tll.xml', 'r') # sys.argv[4] F:\Capstone\AUH\osm\plain\island.tll.xml
dump_file = open('F:\Capstone\AUH\osm\duarouter\island.dump.xml', 'r') # sys.argv[5] F:\Capstone\AUH\osm\duarouter\island.dump.xml

gravity_node_file = open('F:\Capstone\AUH\osm\output\gravity.nod.xml', 'w') # F:\Capstone\AUH\osm\output\gravity.nod.xml
gravity_edge_file = open('F:\Capstone\AUH\osm\output\gravity.edg.xml', 'w') # F:\Capstone\AUH\osm\output\gravity.edg.xml
gravity_con_file = open('F:\Capstone\AUH\osm\output\gravity.con.xml', 'w') # F:\Capstone\AUH\osm\output\gravity.con.xml
gravity_tll_file = open('F:\Capstone\AUH\osm\output\gravity.tll.xml', 'w') # F:\Capstone\AUH\osm\output\gravity.tll.xml

"""
location_list = [] # 1 # keep unchanged
node_list = [] # 8545 # input # output (modified)
edge_list = [] # 17909 # input
roundabout_list = [] # 79 # keep unchanged
edge_weight_list = [] # 17909 # input
"""

# READ NODE FILE TO GET NODES
print "read node file"
node_tree = ET.parse(node_file)
node_root = node_tree.getroot()

"""file_locations = node_root.iter('location')
location_subtree = ET.Element('location_subtree_root')
location_len = 0
for file_location in file_locations:
	location_subtree.append(file_location)
	location_len += 1
locations = location_subtree.iter('location')
print str(location_len)"""

file_nodes = node_root.iter('node')
node_subtree = ET.Element('node_subtree_root')
node_len = 0
for file_node in file_nodes:
	node_subtree.append(file_node)
	node_len += 1
#print str(node_len)

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
#print str(edge_len)

"""file_roundabouts = edge_root.iter('roundabout')
roundabout_subtree = ET.Element('roundabout_subtree_root')
roundabout_len = 0
for file_roundabout in file_roundabouts:
	roundabout_subtree.append(file_roundabout)
	roundabout_len += 1
roundabouts = roundabout_subtree.iter('roundabout')
print str(roundabout_len)"""

# READ CONNECTION FILE TO GET CONNECTIONS (UNCHANGED)
print "read con file"
con_tree = ET.parse(con_file)
#con_root = con_tree.getroot()

# READ TLL FILE TO GET TLLS (UNCHANGED)
print "read tll file"
tll_tree = ET.parse(tll_file)
#tll_root = tll_tree.getroot().find('connection')

# READ DUMP FILE TO GET EDGE WEIGHTS
print "read dump file"
dump_tree = ET.parse(dump_file)
dump_root = dump_tree.getroot().find('interval')

file_dump_edges = dump_root.iter('edge')
dump_edge_subtree = ET.Element('dump_edge_subtree_root')
dump_edge_len = 0
for file_dump_edge in file_dump_edges:
	dump_edge_subtree.append(file_dump_edge)
	dump_edge_len += 1
#print str(dump_edge_len)

# APPLY WEIGHTS TO THE EDGES
print "apply weights to edges"
# assumes that the list of edges exactly matches the list of weighted edges
# is occupancy even the right measure here?
dump_edges = dump_edge_subtree.iter('edge')
edges = edge_subtree.iter('edge')
for dump_edge in dump_edges:
	#print str(dump_edge.get('id'))+" + "+str(dump_edge.get('occupancy'))
	weight = float(dump_edge.get('occupancy',0.0))
	if weight > 100.0: # is this necessary? how can occupancy be >100% though?
		weight = 100.0
	next(edges).set('weight', str(weight))

# APPLY WEIGHTS TO THE NODES
print "apply weights to nodes"
# for each node, add up weights from incoming edges
# actually follow edges because they are the ones that have connection info
# then divide by sum by number of incoming edges
edges = edge_subtree.iter('edge') # reset edges iter
for edge in edges:
	#if edge.get('to') is not None:
	node = node_subtree.find('node[@id=\''+edge.get('to')+'\']') # assumes that the node is present in node list
	node.set('weight_sum',str(float(node.get('weight_sum','0.0'))+float(edge.get('weight')))) # increase node's weight sum by edge's weight
	node.set('weight_num',str(float(node.get('weight_num','0.0'))+1.0)) # increment node's weight num
nodes = node_subtree.iter('node')
for node in nodes:
	node.set('weight',str(float(node.get('weight_sum','0.0'))/float(node.get('weight_num','1.0')))) # average or 0.0 if no data

# GET AVERAGE WEIGHT
print "get average weight"
# add up all weights and divide by number of nodes
# maybe not necessary?
node_weight_sum = 0.0
for node in nodes:
	node_weight_sum += float(node.get('weight','0.0'))
average_weight = node_weight_sum/float(node_len)

# IDENTIFY NEIGHBORS
print "identify neighbors"
# identify nodes' neighbors and how to reach them
edges = edge_subtree.iter('edge') # reset edges iter
for edge in edges:
	source_node = node_subtree.find('node[@id=\''+edge.get('from')+'\']') # assumes that the source node is present in node list
	source_node.append(ET.Element('neighbor', attrib={'id':edge.get('to'),'edge':edge.get('id')})) # add the destination of the edge (edges store their id's) to a list of neighbors of the source node

# ADDED
# IDENTIFY CONNECTED NODES
print "identify connected"
# identify the nodes connected to nodes (reverse neighbors)
edges = edge_subtree.iter('edge') # reset edges iter
for edge in edges:
	target_node = node_subtree.find('node[@id=\''+edge.get('to')+'\']') # assumes that the target node is present in node list
	target_node.append(ET.Element('connected', attrib={'id':edge.get('from'),'edge':edge.get('id')})) # add the source of the edge to list of connected of the target node

# APPLY GRAVITY
print "apply gravity"
# like dijkstra (?) = breadth first
node_set = set() # recordkeeping
edge_set = set() # recordkeeping
for node in node_subtree.iter('node'):
	node_set.add(node.get('id'))
for edge in edge_subtree.iter('edge'):
	edge_set.add(edge.get('id'))

short_distance_overrides = 0 # recordkeeping

element_queue = [] # waiting elements
finished_node_id_list = [] # finished elements

gravity_constant = 1.0 # (works with 1.0/100.0) # determines the scale of output
gravity_exponential = 2.0 # the power of the distance dropoff of gravity (real gravity = 2.0) # determines the smoothness of the deformation of output - smaller = smoother

# start with a node (for example: cluster_261663131_261663132_261707988_261707989 - which is nice because it is compact and approximately in the middle of the corniche); this will be the center of gravity and is the only one that will not move around
initial_node = node_subtree.find('node[@id=\'cluster_261663131_261663132_261707988_261707989\']')
initial_path = [(None,0,None,[],[])] # previous_node, previous_weight, edge_from_previous, distances_from_previous, bearings_from_previous
initial_element = {'node':initial_node,'path':initial_path,'total_distance':0}

node_set.remove(initial_node.get('id'))
element_queue.append(initial_element)

def get_coords(node_from, edge, node_to): # WATCH OUT, THIS WILL RETURN MODIFIED x AND y FOR MODIFIED NODES
	coords = []
	#print 'node_from:'+node_from.get('id')
	#print 'edge:'+edge.get('id')
	#print 'node_to:'+node_to.get('id')
	coords.append((float(node_from.get('x')),float(node_from.get('y'))))
	edge_shape = edge.get('shape','')
	#print 'edge_shape:'+edge_shape
	shape_coord_strs = edge_shape.split()
	for shape_coord_str in shape_coord_strs:
		shape_coords = shape_coord_str.split(',')
		coords.append((float(shape_coords[0]),float(shape_coords[1])))
	coords.append((float(node_to.get('x')),float(node_to.get('y'))))
	return coords

def get_distances(coords):
	# distance along the shape of the edge
	distances = []
	index = 1
	#print coords
	while index < len(coords):
		first_coord = coords[index-1]
		second_coord = coords[index]
		distances.append(math.hypot(abs(first_coord[0]-second_coord[0]),abs(first_coord[1]-second_coord[1]))) # hypotenuse
		index += 1
	#print distances
	return distances

def get_distance(distances):
	distance_sum = 0.0
	for distance in distances:
		distance_sum += distance
	return distance_sum

def get_bearings(coords):
	# bearings to reach each intermediate point between node_from and node_to
	# output values increase counterclockwise from due west; (due west = -pi //not really), due south = -pi/2, due east = 0, due north = pi/2, due west = pi
	# tan(alpha) = opp/adj => tan(alpha) = y/x => arctan(y/x) = alpha # alpha is what is returned in bearings
	bearings = []
	index = 1
	while index < len(coords):
		first_coord = coords[index-1]
		second_coord = coords[index]
		bearings.append(math.atan2(second_coord[1]-first_coord[1],second_coord[0]-first_coord[0])) # atan2 has y,x
		index += 1
	#print coords
	#print bearings
	return bearings

# get the first node from the queue while we have something there
while len(element_queue) != 0:
	current_element = element_queue.pop(0)

	current_node = current_element['node']
	print 'investigating node: '+str(current_node.get('id'))
	current_path = current_element['path']
	current_total_distance = current_element['total_distance']

	current_weight = float(current_node.get('weight'))

	# once we enter a new node, add its neighbors to Q (a queue of nodes, sorted ascending by distance from initial node where distances are along outgoing_edges; if a node is already in Q, rewrite closest distance if current path is shorter); Q has, for each node, the node, and a hierarchy of nodes that signify the path to get there - for each part of the path, keep the distance
	neighbors = current_node.iter('neighbor')
	for neighbor in neighbors:
		print '\tinvestigating neighbor: '+str(neighbor.get('id'))
		if neighbor.get('id') not in finished_node_id_list: # ALSO NEEDS TO CONSIDER ALL EDGES GOING TO NODES THAT HAVE ALREADY BEEN EXPLORED BC OTHERWISE THOSE WOULD STAY UNCHANGED
			print '\t\tnot in finished list'
			neighbor_node = node_subtree.find('node[@id=\''+neighbor.get('id')+'\']')
			edge_from_current = edge_subtree.find('edge[@id=\''+neighbor.get('edge')+'\']')
			neighbor_coords = get_coords(current_node,edge_from_current,neighbor_node)
			distances_from_current = get_distances(neighbor_coords)
			bearings_from_current = get_bearings(neighbor_coords)
			neighbor_path = [(current_node,current_weight,edge_from_current,distances_from_current,bearings_from_current)] # notice that this stores distance before x's and y's are altered
			neighbor_path.extend(current_path[:])
			
			distance_from_current = get_distance(distances_from_current)
			neighbor_total_distance = current_total_distance + distance_from_current
			neighbor_element = {'node':neighbor_node,'path':neighbor_path,'total_distance':neighbor_total_distance}

			index = 0
			inserted = False
			better_in = False
			while index < len(element_queue):
				element = element_queue[index]
				if not inserted and element['total_distance'] > neighbor_element['total_distance']:
					# if we reach an element that is farther than neighbor element's distance, we should insert neighbor at that index (in front of that element)
					print '\t\tneighbor distance lower than element distance (element '+element['node'].get('id')+')'
					edge_set.remove(edge_from_current.get('id'))
					print '\t\t\tused edge1: '+str(edge_from_current.get('id'))+' (edge set len: '+str(len(edge_set))+')'
					node_set.discard(neighbor_node.get('id')) # remove if present # can be already removed if this is a replacement
					print '\t\t\t(node set len: '+str(len(node_set))+')'
					element_queue.insert(index,neighbor_element)
					inserted = True
				if element['node'].get('id') == neighbor_node.get('id'):
					# if we reach the same node as the one we are comparing to...
					if inserted:
						# ...after having inserted same node at better position? - remove the second instance
						print '\t\tneighbor node encountered at worse position than proposed'
						old_element = element_queue.pop(index)
						edge_set.add(old_element['path'][2][0].get('id')) # reinstate the edge used to get there to the list of unused edges
						print '\t\t\treinstating edge: '+str(old_element['path'][2][0].get('id'))+' (edge set len: '+str(len(edge_set))+')'
					else:
						# ...before we would have inserted it at currently explored distance? - do not insert, already at a better option
						print '\t\tneighbor node encountered at better position than proposed'
						better_in = True
					break
				index += 1
			if not inserted and not better_in:
				# if we did not insert and there is no better option in there already
				print '\t\tneighbor node not encountered until end of element queue'
				edge_set.remove(edge_from_current.get('id'))
				print '\t\t\tused edge2: '+str(edge_from_current.get('id'))+' (edge set len: '+str(len(edge_set))+')'
				node_set.remove(neighbor_node.get('id'))
				print '\t\t\t(node set len: '+str(len(node_set))+')'
				element_queue.append(neighbor_element)
		else:
			print '\t\talready in finished list'

	# PATH BASED GRAVITY POTENTIAL CALCULATION
	# for the entered node, get the distance and the gravity potential (a function of weight of previous nodes and their distances according to gravity law)
	# return gravity factor for current node
	distance_along_path = 0.0
	gravity_potential = 0.0
	for path_node,path_weight,edge_from_path,distances_from_path,bearings_from_path in current_path: # NEIGHBOR BASED GRAVITY POTENTIAL: REPLACE BY BREADTH-FIRST SEARCH OF CLOSEST NEIGHBORS IN X
		distance_along_path = get_distance(distances_from_path)
		if path_node is None:
			break
		"""if distance_along_path > 1000000:
			# overflow protection?
			break"""
		distance_exponent = pow(distance_along_path,gravity_exponential)
		new_gravity_potential = gravity_constant*((path_weight*current_weight)/distance_exponent) # SHOULD THIS INCLUDE *CURRENT_WEIGHT?
		if new_gravity_potential < gravity_constant*0.0001:
			# don't continue down previous path if gravity effects are miniscule
			break
		gravity_potential += new_gravity_potential
	gravity_factor = 1.0 / (1.0 + gravity_potential) # multiply distance_to_neighbor by this to get the new desired distance

	# displace the current node = move the x and y towards the immediate predecessor according to distance and gravity factor, keeping the angle constant # ASSUMPTION - NOTICE THAT THIS DOES NOT PRESERVE ANGLES TO ANY NEIGHBORS THAT HAVE ALREADY BEEN DEALT WITH!!
	# keep in mind that the shape elements of the outgoing_node have to change too - this can be uniform based on distance and not scaled for gravity though # SIMPLIFYING ASSUMPTION
	previous_node,previous_weight,edge_from_previous,distances_from_previous,bearings_from_previous = current_path[0]
	new_distances = []
	for distance in distances_from_previous:
		new_distance = distance * gravity_factor
		if new_distance < 0.02:
			# makes sure network can be built (since floats are truncated to two decimal places and nodes must not overlap)
			new_distance = 0.02
			short_distance_overrides += 1
		new_distances.append(new_distance)
	
	if previous_node is not None:
		previous_positions = [float(previous_node.get('x')),float(previous_node.get('y'))] # these are modified for modified elements - expected behavior
	new_positions = [] # contains tuples of xy pairs
	bearings_iter = iter(bearings_from_previous)
	for new_distance in new_distances:
		# we know x and y of previous spot
		previous_x = previous_positions[0]
		previous_y = previous_positions[1]
		# we know the distance to the new spot = hypotenuse
		# we know the atan2 bearing to the new spot = alpha
		bearing_to_new = next(bearings_iter)
		# we want to find out the length of opp and adj		
		# cos(alpha) = adj/hyp => adj = cos(alpha)*hyp => extra_x = cos(alpha)*hyp
		new_x = previous_x + (math.cos(bearing_to_new) * new_distance)
		# sin(alpha) = opp/hyp => opp = sin(alpha)*hyp => extra_y = sin(alpha)*hyp
		new_y = previous_y + (math.sin(bearing_to_new) * new_distance) # REFORMULATE THIS WITHOUT TRIG FUNCTIONS TO BE MORE EFFICIENT
		#print str((previous_x,previous_y))+' -> '+str((new_x,new_y))

		new_positions.append((new_x,new_y))
		previous_positions[0] = new_x
		previous_positions[1] = new_y

	# new_positions[-1] is the new position of current_node = not part of shape_string
	shape_string = ''
	index = 0
	while index < len(new_positions)-1:
		new_position = new_positions[index]
		if index > 0:
			shape_string += ' '
		shape_string += str(new_position[0])+','+str(new_position[1])
		index += 1

	if shape_string is not '':
		edge_from_previous.set('shape',shape_string)

	if len(new_positions) > 0:
		new_current_node_position = new_positions[-1]
		current_node.set('x',str(new_current_node_position[0]))
		current_node.set('y',str(new_current_node_position[1]))

	# (FOR NEIGHBOR BASED) after we are done with the current node, add it to X (queue of nodes FIFO); X has, for each node, the node, and a hierarchy of nodes that signify the path to get there including the distance
	finished_node_id_list.append(current_node.get('id'))
	print 'finished node: '+str(current_node.get('id'))+' ('+str(len(finished_node_id_list))+')'
	# WE DO NOT TOUCH ALL OF THEM - 105 FEWER FINISHED NODES THAN TOTAL NODES

print 'short distance overrides: '+str(short_distance_overrides)

print 'unused nodes: '+str(len(node_set)) # 105 unused ones
#node_index = 0
#for node in node_set:
#	node_index += 1
#	print '\t'+str(node)+' ('+str(node_index)+')'

print 'unused edges: '+str(len(edge_set)) # 9361 unused ones
#edge_index = 0
#for edge in edge_set:
#	edge_index += 1
#	print '\t'+str(edge)+' ('+str(edge_index)+')'

# WRITE OUTPUT FILES
print "write output files"
node_tree.write(gravity_node_file,encoding='UTF-8',xml_declaration=True)
edge_tree.write(gravity_edge_file,encoding='UTF-8',xml_declaration=True)
con_tree.write(gravity_con_file,encoding='UTF-8',xml_declaration=True)
tll_tree.write(gravity_tll_file,encoding='UTF-8',xml_declaration=True)

#gravity_node_root = node_root
#gravity_root.append(location_subtree)
#gravity_root.append(node_subtree)
#gravity_root.append(edge_subtree)
#gravity_root.append(roundabout_subtree)

#gravity_tree = ET.ElementTree(gravity_root)
#gravity_tree.write(gravity_file,encoding='UTF-8',xml_declaration=True)

# CLOSE FILES
print "close files"

node_file.close()
edge_file.close()
con_file.close()
tll_file.close()
dump_file.close()
gravity_node_file.close()
gravity_edge_file.close()
gravity_con_file.close()
gravity_tll_file.close()