
import webcolors
from xml.etree import ElementTree as et
import numpy as np
import os

class Tile(object):
	"""A tile, defined by a set of ellipse parameters and a background color.
	
	Attributes:
		bg_color: (Background color) Any web color name, default is "white".
		fg_color: (Foreground color) Any web color name, default is "black".
		ellipses: A list of ellipse parameters, each a tuple (cx,cy,rx,ry), with:
			cx, cy: centre of the ellipse where the centre with respect to a square tile centred at (0,0) with width = 2;
			rx, ry: horizontal and vertial 'radii' of the ellipse in the same coordinate system.
		name: A codename for the tile. E.g., 'b_ne' for a black-background tile with an ellipse in the NE corner.
		tile_size: A tuple (width,height) giving the dimensions of the tile.
		edge_color_names: A tuple of four colours giving the volour of the (top, right, bottom, left) edges of the tile.
		edge_color_rgbs: Same as above, but with each colour given as an RGB tuple.
	"""
	
	def __init__(self, bg_color="white", fg_color="black", ellipses=[], name="tmp", tile_size=(100,100)):
		self.local_save_dir = "./quilts/tiles"
		self.bg_color = webcolors.name_to_rgb(bg_color)
		self.fg_color = webcolors.name_to_rgb(fg_color)
		self.ellipses = ellipses
		self.name = name
		self.tile_size = tile_size
	
	def __repr__(self):
		return "<Background:%s Foreground:%s Name:%s Size:%s>" % (webcolors.rgb_to_name(self.bg_color), webcolors.rgb_to_name(self.fg_color), self.name, self.tile_size)
		
	def make_tile_path(self):
		return self.local_save_dir + "/" + self.name + "_" + str(self.tile_size[0]) + ".svg"
	
	def get_canvas_coords(self, single_ellipse_coords):
		cx, cy, rx, ry = single_ellipse_coords
		new_cx = (cx+1)/2.0*self.tile_size[0]
		new_cy = (1-cy)/(2.0)*self.tile_size[1]
		new_rx = rx/2.0*self.tile_size[0]
		new_ry = ry/2.0*self.tile_size[1]
		return [new_cx, new_cy, new_rx, new_ry]
	
	def get_ellipse_edge_colors(self):
		# For each edge, check a few points along the edges and verify that all of them or none of them are in any ellipses.
		point_range = np.linspace(-1,1,3)
		top_points = [(x,1) for x in point_range]
		rig_points = [(1,x) for x in point_range]
		bot_points = [(x,-1) for x in point_range]
		lef_points = [(-1,x) for x in point_range]
		colors = [self.get_set_color(point_set,self.ellipses) for point_set in [top_points, rig_points, bot_points, lef_points]]
		return colors
	
	def check_if_point_in_ellipse(self, point, ellipse):
		# A point (x,y) is in an ellipse if (x-cx)^2/a^2 + (y-cy)^2/b^2 < 1,
		# where the ellipse has width a, height b, and its centre is located at (cx,cy).
		x,y = point
		cx,cy,a,b = ellipse
		return (np.power(x-cx,2)/np.power(a,2) + np.power(y-cy,2)/np.power(b,2))
	
	def get_set_color(self, points, ellipses):
		if not ellipses:
			# print "Empty tile, so assigning background color."
			return self.bg_color
		point_tests = np.array([[self.check_if_point_in_ellipse(point, ellipse) for ellipse in self.ellipses] for point in points])
		# Is every point in (or on the edge of) at least one ellipse?
		test_inclusion = np.all([np.min(test_result) <= 1 for test_result in point_tests])
		# Is every point outside (but possibly touching) ALL of the ellipses?
		test_exclusion = np.all([np.min(test_result) >= 1 for test_result in point_tests])
		if (test_inclusion and test_exclusion):
			print "Cannot decide on colour for one edge, since all points in test set are tangent to ellipses. Assigning background colour."
			return self.bg_color
		elif test_inclusion:
			return self.fg_color
		elif test_exclusion:
			return self.bg_color
		elif (not test_inclusion and not test_exclusion):
			print "Cannot decide on colour for one edge, since it fails exclusion and inclusion tests. Assigning background colour."
			return self.bg_color
	
	def imagine_tile_layout(self):
		# Create blank canvas of appropriate size:
		self.doc = et.Element('svg', width=str(self.tile_size[0]), height=str(self.tile_size[1]), version='1.1', xmlns='http://www.w3.org/2000/svg')
		# Paint in the background rectangle:
		bg_color_string = 'rgb({0}, {1}, {2})'.format(self.bg_color[0],self.bg_color[1],self.bg_color[2])
		fg_color_string = 'rgb({0}, {1}, {2})'.format(self.fg_color[0],self.fg_color[1],self.fg_color[2])
		et.SubElement(self.doc, 'rect', width=str(self.tile_size[0]), height=str(self.tile_size[1]), fill=bg_color_string)
		# , stroke=bg_color_string)
		# self.doc[-1].set("stroke-width","2")
		# Paint in the foreground circles:
		for single_ellipse_coords in self.ellipses:
			[cx, cy, rx, ry] = self.get_canvas_coords(single_ellipse_coords)
			et.SubElement(self.doc, 'ellipse', cx=str(cx), cy=str(cy), rx=str(rx), ry=str(ry), fill=fg_color_string)
			# , stroke=fg_color_string)
			# self.doc[-1].set("stroke-width","2")
		# for i in range(len(self.doc)):
		# 	for j in range(len(self.doc[i].keys())):
		# 		if self.doc[i].keys()[j]=="stroke_width":
		# 			self.doc[i].keys()[j]="stroke-width"
	
	def write_tile_layout(self):
		f = open(self.make_tile_path(), 'w')
		f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
		f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
		f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
		f.write(et.tostring(self.doc))
		f.close()
	
	def create_tile_image(self, overwrite=False):
		if (not os.path.exists(self.make_tile_path())) or (overwrite==True):
			self.imagine_tile_layout()
			self.write_tile_layout()

# Demo of the Tile object:
# 
# a = Tile(bg_color="white", fg_color="red", ellipses=[(-1,0,1.1,1), (1,0,1.1,1)], name="tmp")
# a.create_tile_image()
# a.get_ellipse_edge_colors()


import svgwrite

class Quilt(object):
	"""A grid of tiles, each generated by a Tile object.
	
	Attributes:
		grid_size: (width, height), in numbers of tiles
		tile_sie: (width, height) of each tile
		bg_color: Any web color name, default is "white".
		fg_color: Any web color name, default is "black".
		name: Filename for saving.
	"""
	
	def __init__(self, grid_size=(20,10), tile_size=(50, 50), bg_colors=["white"], fg_colors=["black"], tile_groups=["basic","2s"], name="tmp_quilt", edge_command=None):
		self.local_save_dir = "."
		self.grid_w, self.grid_h = grid_size
		self.tile_w, self.tile_h = tile_size
		self.page_w, self.page_h = self.grid_w * self.tile_w, self.grid_h * self.tile_h
		# self.bg_color = webcolors.name_to_rgb(bg_color)
		# self.fg_color = webcolors.name_to_rgb(fg_color)
		self.name = name
		self.fg_colors = fg_colors
		self.bg_colors = bg_colors
		self.tile_groups = tile_groups
		self.edge_command = edge_command
		self.reset_quilt()
		# (Top, Right, Bottom, Left)
	
	def __repr__(self):
		return "<Background:%s Foreground:%s Tiles:%s Edges:%s>" % (self.bg_colors, self.fg_colors, self.tile_groups, self.edge_command)
		
	def reset_quilt(self):
		self.tile_ids = np.zeros((self.grid_h,self.grid_w)).astype(int)-1
		self.tile_constraints = np.zeros((self.grid_h, self.grid_w, 4, 3))-1
		self.tile_set = []
		self.tile_edge_colors = np.zeros((0,4,3))
		self.add_tile_designs()
		self.set_edges()
	
	def set_edges(self):
		if self.edge_command is None:
			top=right=bottom=left=[self.bg_colors[0],self.fg_colors[0]]
		else:
			if len(self.edge_command)==1:
				top=right=bottom=left=self.edge_command[0]
			elif len(self.edge_command)==2:
				top=bottom=self.edge_command[0]
				right=left=self.edge_command[1]
			elif len(self.edge_command)==4:
				top,right,bottom,left = self.edge_command
		self.edge_swatches = {"t":top,"r":right,"b":bottom,"l":left}
	
	def make_quilt_path(self):
		return self.local_save_dir + "/" + self.name + ".svg"
	
	def add_tile_designs(self, fg_colors=None, bg_colors=None, tile_groups=None):
		# ["basic","1s","2s","3s","solids"]):
		if fg_colors is None:
			fg_colors = self.fg_colors
		if bg_colors is None:
			bg_colors = self.bg_colors
		if tile_groups is None:
			tile_groups = self.tile_groups
		import itertools
		# Original set of tiles
		# if len(color_set)==1:
		# 	for fg_color,bg_color in itertools.permutations(color_set[0], 2):
		# 		self.add_tile_designs(color_set=[[fg_color],[bg_color]], tile_groups=tile_groups)
		# 	return
		# 	# fg_colors = color_set[0]
		# 	# bg_colors = color_set[0]
		# elif len(color_set)==2:
		# 	fg_colors, bg_colors = color_set
		# elif len(color_set)>2:
		# 	print "Error! Ill-formatted color set."
		tile_set = []
		if "solids" in tile_groups:
			for bg_color in bg_colors:
				tile_set += [Tile(bg_color=bg_color, fg_color=bg_color, ellipses=[], name=bg_color+"_solid")]
		color_combos = list(itertools.product(fg_colors, bg_colors+fg_colors))
		for fg_color,bg_color in color_combos:
			if fg_color==bg_color:
				tile_set += [Tile(bg_color=bg_color, fg_color=bg_color, ellipses=[], name=bg_color+"_solid")]
			else:
			# for fg_color,bg_color in itertools.permutations(color_set, 2):
				name_stem = fg_color + "_on_" + bg_color + "_"
				if "basic" in tile_groups:
					labels = ['ne','nw','sw','se']
					center_y = np.array([1-2*(label[0]=="s") for label in labels])
					center_x = np.array([2*(label[1]=="e")-1 for label in labels])
					for i,label in enumerate(labels):
						tile_set += [Tile(bg_color=bg_color, fg_color=fg_color, ellipses=[(center_x[i],center_y[i],2,2)], name=name_stem+label)]
				labels = []
				if "1s" in tile_groups:
					labels += ['n','e','s','w']
				if "2s" in tile_groups:
					labels += ['ns','ew']
				if "3s" in tile_groups:
					labels += ['nes','new','nsw','esw']
				circle_coords = {'n': [0,-1], 'e': [1,0], 's': [0,1], 'w':[-1,0], 'x':[3,3]}
				# canvas_coords = {key:[0,0] for key in circle_coords.keys()}
				for i,label in enumerate(labels):
					tmp_tile = Tile(bg_color=bg_color, fg_color=fg_color, ellipses=[], name=name_stem+label)
					for letter in label:
						tmp_tile.ellipses += [(circle_coords[letter][0],circle_coords[letter][1],1,1)]
					tile_set += [tmp_tile]
			for tmp_tile in tile_set:
				tmp_tile.create_tile_image()
		self.tile_set += tile_set
		# edge_colors[i,j,:] gives the RGB values for the color of the jth edge (clockwise from top) of the ith tile.
		new_edge_colors = np.array([tmp_tile.get_ellipse_edge_colors() for tmp_tile in tile_set])
		self.tile_edge_colors = np.concatenate((self.tile_edge_colors, new_edge_colors))
	
	def create_random_quilt(self):
		self.tile_ids = np.random.randint(len(self.tile_set),size=self.tile_ids.shape)
	
	# def add_quilt_edge_constraints(self, constraint_list = [[["black"],"tlbr"]]):
	def implement_edge_constraints(self):
		for side in self.edge_swatches.keys():
			if len(self.edge_swatches[side])>0:
				tmp_cols = np.array([np.array(webcolors.name_to_rgb(color)) for color in self.edge_swatches[side]])
				tmp_repmat = np.tile(tmp_cols,reps=(np.max((self.grid_h,self.grid_w)),1))
				if side=="t":
					# Along top row, top edge must be white:
					self.tile_constraints[0,:,0,:] = tmp_repmat[:self.tile_constraints.shape[1],:]
				if side=="l":
					# Along left edge, left edge must be white:
					self.tile_constraints[:,0,3,:] = tmp_repmat[:self.tile_constraints.shape[0],:]
				if side=="b":
					# Ditto for bottom and right:
					self.tile_constraints[-1,:,2,:] = tmp_repmat[:self.tile_constraints.shape[1],:]
				if side=="r":
					self.tile_constraints[:,-1,1,:] = tmp_repmat[:self.tile_constraints.shape[0],:]		
		# This is for defining constraints OUTSIDE the quilt --- i.e., what the quilt edges can possibly be.
		# In order to control INTERNAL constraints --- i.e., how tiles can be arranged on the page --- look elsewhere.
		# If a constraint triplet value is all -1s, it is unconstrained.
		# If a constraint triplet is set, then that edge (top,right,bottom,left) is constrained to equal that value.
		# for constraint in constraint_list:
		# 	color_swatch = constraint[0]
		# 	sides = constraint[1]
		# 	# if "all" in sides:
		# 	# 	sides = ["top","right","bottom","left"]
		# 	tmp_cols = np.array([np.array(webcolors.name_to_rgb(color)) for color in color_swatch])
		# 	tmp_repmat = np.tile(tmp_cols,reps=(np.max((self.grid_h,self.grid_w)),1))
		# 	if "t" in sides:
		# 		# Along top row, top edge must be white:
		# 		self.tile_constraints[0,:,0,:] = tmp_repmat[:self.tile_constraints.shape[1],:]
		# 	if "l" in sides:
		# 		# Along left edge, left edge must be white:
		# 		self.tile_constraints[:,0,3,:] = tmp_repmat[:self.tile_constraints.shape[0],:]
		# 	if "b" in sides:
		# 		# Ditto for bottom and right:
		# 		self.tile_constraints[-1,:,2,:] = tmp_repmat[:self.tile_constraints.shape[1],:]
		# 	if "r" in sides:
		# 		self.tile_constraints[:,-1,1,:] = tmp_repmat[:self.tile_constraints.shape[0],:]
		# self.tile_constraints = tile_constraints
		# Set up a solid outside white border
		# tile_ids[grid_w-1,:] = 3
		# tile_ids[:,grid_h-1] = 3
		# Set up an alternating border
		# tile_ids[grid_w-1,:] = [[1,3][np.mod(i,2)] for i in range(grid_h)]
		# tile_ids[:,grid_h-1] = [[1,3][np.mod(i,2)] for i in range(grid_w)]
	
	def build_out_constrained_quilt(self):
		for i in range(self.grid_h):
			for j in range(self.grid_w):
				if self.tile_ids[i,j]<0:
					current_constraints = self.tile_constraints[i,j]
					if np.any(current_constraints>=0):
						edge_matches = self.tile_edge_colors==current_constraints
						edge_irrelev = np.ones_like(self.tile_edge_colors) * current_constraints<0
						available_edges = [k for k in range(len(self.tile_set)) if np.all(edge_matches[k,:,:]+edge_irrelev[k,:,:])]
					else:
						available_edges = range(len(self.tile_set))
					if len(available_edges)==0:
						# print "No options, reached a logical impasse."
						edge_colors = [webcolors.rgb_to_name(list(int(j) for j in color)) for color in current_constraints]
						print "No tiles match: " + "/".join(edge_colors)
					else:
						tile_id = available_edges[np.random.randint(len(available_edges))]
						self.tile_ids[i,j] = tile_id
						self.tile_constraints[i,j,:,:] = np.array(self.tile_set[tile_id].get_ellipse_edge_colors())
						# Now, tell neighbouring unset cells to have the correct edge colors.
						if i<self.grid_h-1:
							self.tile_constraints[i+1,j,0,:] = self.tile_constraints[i,j,2,:]
						if j<self.grid_w-1:
							self.tile_constraints[i,j+1,3,:] = self.tile_constraints[i,j,1,:]
						if i>0:
							self.tile_constraints[i-1,j,2,:] = self.tile_constraints[i,j,0,:]
						if j>0:
							self.tile_constraints[i,j-1,1,:] = self.tile_constraints[i,j,3,:]
	
	def build_out_constrained_quilt_with_reverse_steps(self, lookback_depth=1):
		coords = [x[0] for x in zip(itertools.product(range(self.grid_h),range(self.grid_w)))]
		fail_counts = np.zeros(len(coords))
		coord_i = 0
		while coord_i < len(coords):
			i,j = coords[coord_i]
			if self.tile_ids[i,j]>=0:
				coord_i += 1
			else:
				current_constraints = self.tile_constraints[i,j]
				if np.any(current_constraints>=0):
					edge_matches = self.tile_edge_colors==current_constraints
					edge_irrelev = np.ones_like(self.tile_edge_colors) * current_constraints<0
					available_edges = [k for k in range(len(self.tile_set)) if np.all(edge_matches[k,:,:]+edge_irrelev[k,:,:])]
				else:
					available_edges = range(len(self.tile_set))
				if len(available_edges)==0:
					fail_counts[coord_i] += 1
					if fail_counts[coord_i]>50:
						print "Failing hard on step " + str(coords[coord_i]) + ". Giving up [this iteration]."
						return
					# FAILURE: iterate back one.
					# print "No options, reached a logical impasse."
					edge_colors = [webcolors.rgb_to_name(list(int(j) for j in color)) for color in current_constraints]
					print "No tiles match: " + "/".join(edge_colors)
					if coord_i == 0:
						print "Infeasible from the outset."
						return
					else:
						coord_i -= 1
						i,j = coords[coord_i]
						self.tile_ids[i,j] = -1
				else:
					# SUCCESS: pick a tile and move on.
					tile_id = available_edges[np.random.randint(len(available_edges))]
					self.tile_ids[i,j] = tile_id
					self.tile_constraints[i,j,:,:] = np.array(self.tile_set[tile_id].get_ellipse_edge_colors())
					# Now, tell neighbouring unset cells to have the correct edge colors.
					if i<self.grid_h-1:
						self.tile_constraints[i+1,j,0,:] = self.tile_constraints[i,j,2,:]
					if j<self.grid_w-1:
						self.tile_constraints[i,j+1,3,:] = self.tile_constraints[i,j,1,:]
					if i>0:
						self.tile_constraints[i-1,j,2,:] = self.tile_constraints[i,j,0,:]
					if j>0:
						self.tile_constraints[i,j-1,1,:] = self.tile_constraints[i,j,3,:]
	
	# Force build
	def build_out_constrained_quilt_harder(self, max_iters=50):
		self.reset_quilt()
		iters = 0
		while np.any(self.tile_ids<0):
			self.reset_quilt()
			self.implement_edge_constraints()
			# self.add_quilt_edge_constraints(constraint_list)
			self.build_out_constrained_quilt_with_reverse_steps()
			iters += 1
			if np.mod(iters,50)==49:
				print iters+1
			if max_iters<iters:
				print "Sorry, we tried hard but could not make it work. Halting."
				return False
		return True
	
	def write_quilt(self, name=None):
		if name:
			self.name = name
		dwg = svgwrite.Drawing(filename = self.make_quilt_path(), size = (str(self.page_w)+"px", str(self.page_h)+"px"))
		for i in range(self.grid_w):
			for j in range(self.grid_h):
				x_i = i*self.tile_w-.1
				x_j = j*self.tile_h-.1
				lab_k = self.tile_ids[j,i]
				subimage_path = self.tile_set[lab_k].make_tile_path()
				image = svgwrite.image.Image(subimage_path, insert=(x_i,x_j), size=(self.tile_w+.2,self.tile_h+.2))
				image.stretch()
				dwg.add(image)
		dwg.save()


# Example usage:
# q = Quilt(grid_size=(9,9), tile_groups=["basic","solids","2s"], fg_colors=["blue","black"], edge_command=[["white","black"],["white","black"],["white","black"],["white","blue"]])
# q.reset_quilt()
# q.implement_edge_constraints()
# flag = q.build_out_constrained_quilt_harder()
# if flag:
# 	q.write_quilt()

# # # # Create a sequence of images to post:
# def try_hard_to_make_tile(quilt, constraint_list, max_iters=1000):
# 	quilt.reset_quilt()
# 	iters = 0
# 	while np.any(quilt.tile_ids<0):
# 		quilt.reset_quilt()
# 		quilt.add_quilt_edge_constraints(constraint_list)
# 		quilt.build_out_constrained_quilt()
# 		iters += 1
# 		if max_iters<iters:
# 			print "Sorry, we tried hard but could not make it work. Halting."
# 			return quilt
# 	return quilt



# TODO:
# Handle SVG -> PNG or JPG conversion 
# Create tiles in a more logical way --- i.e., don't dumbly brute-force as in try_hard_to_make_tile
# Create way to make constraint sequences to generate tiles according to concisely-stated paths.

class QuiltSequence(object):
	"""A sequence of Quilts, each of which is a random collection of Tiles.
	
	Attributes:
		n_columns = 3 (assumed by default for Instagram-like three-column layout, but modifiable)
		name: Filename for saving.
		grid_size: (width, height) of grids, in number of tiles
		tile_size: (width, height) of tiles, in pixels
	"""
	
	def __init__(self, seed_quilt, name="tmp_qseq", n_columns=3):
		self.local_save_dir = "."
		self.n_columns = n_columns
		self.name = name
		self.quilt_sequence = [seed_quilt]
		self.quilt_sequence[0].name = self.name+"0"
		self.qs=self.quilt_sequence
	
	def clone_last_quilt(self):
		import copy
		return copy.deepcopy(self.quilt_sequence[-1])
	
	def extend_sequence(self, left_edge_swatch=[], top_edge_swatch=[], reps=1, tile_groups=[], fg_colors=[], bg_colors=[]):
		if reps>1:
			for i in range(reps):
				self.extend_sequence(left_edge_swatch=left_edge_swatch, top_edge_swatch=top_edge_swatch, reps=1, tile_groups=tile_groups, fg_colors=fg_colors, bg_colors=bg_colors)
			return
		else:
			new_quilt = self.clone_last_quilt()
			n = len(self.quilt_sequence)
			#
			# Set new quilt edges
			#
			# First, set right edge to be previous quilt's left edge, so they match.
			new_quilt.edge_swatches['r'] = new_quilt.edge_swatches['l']
			# If quilt is in bottom row, no need to update bottom edge constraint.
			# If not, set it to lower_neighbour's top edge.
			if n >= self.n_columns:
				lower_neighbour = self.quilt_sequence[n-self.n_columns]
				new_quilt.edge_swatches['b'] = new_quilt.edge_swatches['t']
			if len(left_edge_swatch) > 0:
				new_quilt.edge_swatches['l'] = left_edge_swatch
			if len(top_edge_swatch) > 0:
				new_quilt.edge_swatches['t'] = top_edge_swatch
			# Write the nwe edge swatches into the quilt's edge_command:
			new_quilt.edge_command = [new_quilt.edge_swatches[key] for key in ['t','r','b','l']]
			#
			# Set other quilt properties
			#
			new_quilt.name = self.name + str(len(self.quilt_sequence))
			if  len(tile_groups)>0:
				new_quilt.tile_groups = tile_groups
			if  len(fg_colors)>0:
				new_quilt.fg_colors = fg_colors
			if  len(bg_colors)>0:
				new_quilt.bg_colors = bg_colors
			self.quilt_sequence += [new_quilt]
	
	def implement(self):
		for qi,q in enumerate(self.quilt_sequence):
			print qi
			# q = Quilt(grid_size=(9,9), tile_groups=["basic","solids","2s"], fg_colors=["blue","black"], edge_command=[["white","black"],["white","black"],["white","black"],["white","blue"]])
			q.reset_quilt()
			q.implement_edge_constraints()
			flag = q.build_out_constrained_quilt_harder()
			if flag:
				q.write_quilt()

