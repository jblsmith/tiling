# # # 1. Generate base set of tiles

from xml.etree import ElementTree as et

labels = ['b_ne','b_nw','b_sw','b_se','w_ne','w_nw','w_sw','w_se']
circle_color = [label[0]=="w" for label in labels]
height = 120
width = 120
center_x = [width*(label[-1]=="e") for label in labels]
center_y = [height*(label[-2]=="s") for label in labels]

for i,label in enumerate(labels):
	doc = et.Element('svg', width='120', height='120', version='1.1', xmlns='http://www.w3.org/2000/svg')
	# if label[0]=="w":
	# 	bg_color="black"
	# elif label[0]=="b":
	# 	bg_color="white"
	color=255*circle_color[i]
	bg_color = 255-color
	et.SubElement(doc, 'rect', width=str(width), height=str(height), fill='rgb({0}, {1}, {2})'.format(bg_color,bg_color,bg_color))
	et.SubElement(doc, 'circle', cx=str(center_x[i]), cy=str(center_y[i]), r=str(height), fill='rgb({0}, {1}, {2})'.format(color,color,color))
	f = open(label+'.svg', 'w')
	f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
	f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
	f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
	f.write(et.tostring(doc))
	f.close()

# Reference:
# # Simple SVG writing "by hand": http://nick.onetwenty.org/index.php/2010/04/07/creating-svg-files-with-python/
# # create an SVG XML element (see the SVG specification for attribute details)
# doc = et.Element('svg', width='120', height='120', version='1.1', xmlns='http://www.w3.org/2000/svg')
# # add a circle (using the SubElement function)
# et.SubElement(doc, 'circle', cx='120', cy='120', r='120', fill='rgb(0, 0, 0)')
# # add text (using append function)
# text = et.Element('text', x='240', y='180', fill='white', style='font-family:Sans;font-size:48px;text-anchor:middle;dominant-baseline:top')
# text.text = 'pink circle'
# doc.append(text)
# # ElementTree 1.2 doesn't write the SVG file header errata, so do that manually
# f = open('sample.svg', 'w')
# f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
# f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
# f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
# f.write(et.tostring(doc))
# f.close()


# # # 2. Create script that assembles tiles randomly into larger images.
import scipy as sp
import svgwrite

grid_w = 20
grid_h = 10
tile_w = 50
tile_h = 50
page_w = grid_w * tile_w
page_h = grid_h * tile_h

dwg = svgwrite.Drawing(filename = "./tmp_tile_grid.svg", size = (str(page_w)+"px", str(page_h)+"px"))
for i in range(grid_w):
	for j in range(grid_h):
		x_i = i*tile_w
		x_j = j*tile_h
		lab_k = sp.random.randint(len(labels))
		image = svgwrite.image.Image("./"+labels[lab_k]+".svg", insert=(x_i,x_j), size=(tile_w,tile_h))
		image.stretch()
		dwg.add(image)

dwg.save()

# # # 3. Create script that assembles tiles iteratively according to continuity conditions.

import numpy as np

# Recall from earlier:
labels = ['b_ne','b_nw','b_sw','b_se','w_ne','w_nw','w_sw','w_se']
# left / up / right / down colors of each tile:
edge_colors = np.zeros((len(labels),5)).astype(int)
# First, assume white background
# black = 0
# white = 1
edge_colors[:,0] = [1*(label[-1]=="e") for label in labels]
edge_colors[:,1] = [1*(label[-2]=="s") for label in labels]
edge_colors[:,2] = 1-edge_colors[:,0]
edge_colors[:,3] = 1-edge_colors[:,1]
edge_colors[4:,:] = 1-edge_colors[4:,:]
edge_colors[:,4] = range(edge_colors.shape[0])

# Create a planned layout of tile IDs
import scipy as sp
import svgwrite

grid_w = 20
grid_h = 10
tile_w = 50
tile_h = 50
page_w = grid_w * tile_w
page_h = grid_h * tile_h

tile_ids = np.zeros((grid_w,grid_h)).astype(int)-1
tile_ids[grid_w-1,grid_h-1] = sp.random.randint(len(labels))

# Set up a solid outside white border
# tile_ids[grid_w-1,:] = 3
# tile_ids[:,grid_h-1] = 3

# Set up an alternating border
# tile_ids[grid_w-1,:] = [[1,3][np.mod(i,2)] for i in range(grid_h)]
# tile_ids[:,grid_h-1] = [[1,3][np.mod(i,2)] for i in range(grid_w)]

for i in reversed(range(grid_w)):
	for j in reversed(range(grid_h)):
		if tile_ids[i,j]<0:
			right_id = -1
			under_id = -1
			available_edges = edge_colors[:,:]
			if i<grid_w-1:
				right_id = tile_ids[i+1,j]
				# Only keep options where right edge is the same as left edge of tile to the right
				available_edges = available_edges[available_edges[:,2]==edge_colors[right_id,0],:]
			if j<grid_h-1:
				under_id = tile_ids[i,j+1]
				# Only keep options where bottom edge is the same as the top edge of the tile underneath
				available_edges = available_edges[available_edges[:,3]==edge_colors[under_id,1],:]
			if np.min(available_edges.shape)==0:
				print "No options, reached a logical impasse."
			else:
				tile_ids[i,j] = available_edges[sp.random.randint(available_edges.shape[0]),4]

# tile_constraints = np.zeros(tile_ids.shape+[4])-1
# If constraint is -1, there's no sontraint
# Else, constraint is that tile edge color value equals value

dwg = svgwrite.Drawing(filename = "./constrained_grid.svg", size = (str(page_w)+"px", str(page_h)+"px"))
for i in range(grid_w):
	for j in range(grid_h):
		x_i = i*tile_w
		x_j = j*tile_h
		lab_k = tile_ids[i,j]
		image = svgwrite.image.Image("./"+labels[lab_k]+".svg", insert=(x_i,x_j), size=(tile_w,tile_h))
		image.stretch()
		dwg.add(image)

dwg.save()


# # # 4. Create grids with new types of tiles

# More tiles:
# solids:
# labels = ['b_n+s','b_e+w','w_n+s','w_e+w']
# 'b_n','b_e','b_s','b_w',
# 'w_n','w_e','w_s','w_w',

from xml.etree import ElementTree as et

# circle_color = [label[0]=="w" for label in labels]
height = 120
width = 120
# center_x = [width*(label[-1]=="e") for label in labels]
# center_y = [height*(label[-2]=="s") for label in labels]

def write_elementtree(doc, filename):
	f = open(filename, 'w')
	f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
	f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
	f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
	f.write(et.tostring(doc))
	f.close()


labels = ['','n','e','s','w','ns','ew','nes','new','nsw','esw']
circle_coords = {'n': [0,-1], 'e': [1,0], 's': [0,1], 'w':[-1,0]}
canvas_coords = {key:[0,0] for key in circle_coords.keys()}
for key in circle_coords:
	x,y = circle_coords[key]
	canvas_coords[key] = [x*width*0.5+width*0.5,y*height*0.5 + height*0.5]

for bg_color_name in ['b','w']:
	for i,label in enumerate(labels):
		doc = et.Element('svg', width=str(width), height=str(height), version='1.1', xmlns='http://www.w3.org/2000/svg')
		# color=255*circle_color[i]
		# bg_color = 255-color
		bg_color = 255*(bg_color_name=="w")
		color = 255-bg_color
		et.SubElement(doc, 'rect', width=str(width), height=str(height), fill='rgb({0}, {1}, {2})'.format(bg_color,bg_color,bg_color))
		for letter in label:
			et.SubElement(doc, 'circle', cx=str(canvas_coords[letter][0]), cy=str(canvas_coords[letter][1]), r=str(height/2), fill='rgb({0}, {1}, {2})'.format(color,color,color))
		filename = bg_color_name + "_mini-" + label
		write_elementtree(doc, filename)

# In order to handle a larger list of tile types, we create an Tile class to generate tiles and handle the logic of their edges.









def powerset(iterable):
    # "list(powerset([1,2,3])) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

tile_group_opts = [list(t) for t in powerset(["basic","1s","2s","3s"]) if len(t)>1]
# Actual sequence:
seed_quilt = tiles.Quilt(grid_size=(9,9), tile_groups=tile_group_opts[0], fg_colors=["black"], bg_colors=["white"], edge_command=[["white","black"],["white"],["white"],["white","black"]])
seq = tiles.QuiltSequence(seed_quilt, name="black_and_white", n_columns=3)
seq.extend_sequence(reps=2)
for tg in tile_group_opts:
	seq.extend_sequence(reps=3, tile_groups=tg)

for tg in tile_group_opts:
	seq.extend_sequence(reps=3, tile_groups=tg, fg_colors=["black","white"], bg_colors=["black","white"])

flags = seq.implement(max_iters=20)

# seq.extend_sequence(reps=4)
# seq.extend_sequence(reps=6,fg_colors=["black","yellow"])
seq.extend_sequence(reps=6,fg_colors=["black","white"], tile_groups=["basic"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","basic"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","solid"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","solid","basic"])
seq.extend_sequence(reps=6,fg_colors=["black","yellow","white"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","basic"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","solid"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","solid","basic"])
seq.extend_sequence(reps=6,fg_colors=["black","yellow"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","basic"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","solid"])
seq.extend_sequence(reps=6,tile_groups=["1s","2s","3s","solid","basic"])
flags = seq.implement()
flags = seq.implement(indices=np.where(flags==0)[0])


flags3 = seq.implement(indices=range(10,15))





sequence = tiles.QuiltSequence(q,name="seagreen_seq",n_columns=3)
sequence.extend_sequence(reps=5)
sequence.extend_sequence(fg_colors=["black"], reps=6)
flags = sequence.implement()
for q in sequence.qs:
	q.post_to_tumblr()



# Defining a quilt sequence:
seed_quilt = tiles.Quilt(grid_size=(9,9), tile_groups=["basic","solids","2s"], fg_colors=["red","black"], edge_command=[["white","black"],["white","red"],["white","red"],["white","black"]],verbose=False)
sequence = tiles.QuiltSequence(seed_quilt, name="tmp_sequence", n_columns=3)
sequence.extend_sequence(left_edge_swatch=['white','black'])
sequence.extend_sequence()
sequence.extend_sequence()
sequence.extend_sequence(left_edge_swatch=["white","red"],top_edge_swatch=["white","red"])
sequence.extend_sequence(top_edge_swatch=["white","red"])
sequence.extend_sequence(top_edge_swatch=["white","red"])
sequence.extend_sequence()
flags = sequence.implement()
for qi,i in enumerate(flags):
	if not i:
		print qi
		flags[qi] = sequence.qs[qi].build_out_constrained_quilt_harder()

for q in sequence.qs:
	q.post_to_tumblr(None)




.post-footer { margin-bottom:0px; display:none;}
.caption { display:none; }
.post .inline-meta.post-extra { margin-bottom:0px; padding-bottom:0px;}
.post .inline-meta.post-extra.has-tags {display: none;}




q = tiles.Quilt(grid_size=(9,9), tile_groups=["basic"], fg_colors=["black"], bg_colors=["white"], edge_command=[["white","black"]])
flag = q.build_out_constrained_quilt_harder()
if flag:
	q.write_quilt()


# Pseudocode:
# my_seq = QuiltSequence(grid_size=(9,9), tile_size=(50,50), name='my_quilt', bottom_edge_swatch=["white"], right_edge_swatch=["white"])

seed_quilt = Quilt(grid_size=(9,9), tile_groups=["basic","solids","1s","2s","3s"], fg_colors=["black"], edge_command=[["white","black"], ["white"], ["white"], ["white","black"]])
my_seq = QuiltSequence(seed_quilt, name="tmp_qseq", n_columns=3)
my_seq.extend_sequence(left_edge_swatch=['white','black'])
for i in range(1,5):
	my_seq.extend_sequence(left_edge_swatch=["white"]*i+["black"])
	# my_seq.extend_sequence(left_edge_swatch=['white'])

my_seq.implement()



seed_quilt = Quilt(grid_size=(9,9), tile_groups=["basic","solids","1s","2s","3s"], fg_colors=["black"],  bg_colors=["white"], edge_command=[["white","black"]])
my_seq = QuiltSequence(seed_quilt, name="rainbow", n_columns=3)
# my_seq.implement()
for i in range(1):
	my_seq.extend_sequence(left_edge_swatch=["white","yellow"], fg_colors=["black","yellow"])
	my_seq.extend_sequence(left_edge_swatch=["white","aqua"], fg_colors=["black","yellow","aqua"])
	my_seq.extend_sequence(left_edge_swatch=["white","magenta"], fg_colors=["black","aqua","magenta"])
	my_seq.extend_sequence(left_edge_swatch=["white","black"], fg_colors=["magenta","black"])

my_seq.implement()


def powerset(iterable):
    "list(powerset([1,2,3])) --> [(), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3)]"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

tile_group_opts = [list(t) for t in powerset(["solids","1s","2s","3s"]) if len(t)>1]

tile_group_opts = [x for x in powerset(["basic","1s","2s","3s"])][1:]
seed_quilt = Quilt(grid_size=(9,9), tile_groups=tile_group_opts[0], fg_colors=["black"],  bg_colors=["white"], edge_command=[["white","black"]])
my_seq = QuiltSequence(seed_quilt, name="b&w", n_columns=3)
for tile_group in tile_group_opts[1:]:
	my_seq.extend_sequence(tile_groups=tile_group)

my_seq.implement()





seed_quilt = Quilt(grid_size=(9,9), tile_groups=["3s","solids"], fg_colors=["black","white"],  bg_colors=["white","black"], edge_command=[["white","black"]])
my_seq = QuiltSequence(seed_quilt, name="simple--", n_columns=3)
my_seq.extend_sequence(reps=10)
my_seq.implement()

# my_seq.implement()
for i in range(1):
	my_seq.extend_sequence(left_edge_swatch=["white","yellow"], fg_colors=["black","yellow"])
	my_seq.extend_sequence(left_edge_swatch=["white","aqua"], fg_colors=["black","yellow","aqua"])
	my_seq.extend_sequence(left_edge_swatch=["white","magenta"], fg_colors=["black","aqua","magenta"])
	my_seq.extend_sequence(left_edge_swatch=["white","black"], fg_colors=["magenta","black"])

my_seq.implement()

		
	# def setup_new_quilt(self, bg_colors=None, fg_colors=None, designs=None):
	#
	# 	q = Quilt(grid_size = self.grid_size, tile_size=self.tile_size)
	# 	if bg_colors is None:
	# 		bg_colors = self.bg_colors
	# 	if fg_colors is None:
	# 		fg_colors = self.fg_colors
	# 	if designs is None:
	# 		designs = self.designs
	# 	q.add_tile_designs(color_set=[fg_colors,bg_colors], tile_groups=designs)
	# 	return q
	
	# def extend_sequence(self, left_edge_swatch=[], top_edge_swatch=[]):
	# 	new_quilt = self.clone_last_quilt()
	# 	n = len(self.quilt_sequence)
	# 	if n < self.n_columns:
	# 		# This quilt is in the bottom row, so we need to provide the bottom edge constraint.
	# 		new_quilt.add_quilt_edge_constraints([ [self.bottom_edge_swatch,'b'] ])
	# 	else:
	# 		# We need the top edge of the tile beneath it to get our constraint.
	# 		lower_neighbour = self.quilt_sequence[n-self.n_columns]
	# 		# lower_neighbour is a Quilt object
	# 		new_quilt.add_quilt_edge_constraints([ [lower_neighbour.edge_swatches['t'],'b'] ])
	# 	if n == 0:
	# 		# This is our first quilt, so we need to provide the right edge too.
	# 		new_quilt.add_quilt_edge_constraints([ [self.right_edge_swatch,'l'] ])
	# 	else:
	# 		# We need the right edge of the tile to the right.
	# 		right_neighbour = self.quilt_sequence[n-1]
	# 		new_quilt.add_quilt_edge_constraints([ [right_neighbour.edge_swatches['l'],'r'] ])
	# 	# That's bottom and left done. Now we do top and right:
	# 	# Default behaviour: propagate edges.
	# 	if len(left_edge_swatch) == 0:
	# 		new_quilt.add_quilt_edge_constraints([ [new_quilt.edge_swatches['r'],'l'] ])
	# 	else:
	# 		new_quilt.add_quilt_edge_constraints([ [left_edge_swatch,'l'] ])
	# 	if len(top_edge_swatch) == 0:
	# 		new_quilt.add_quilt_edge_constraints([ [new_quilt.edge_swatches['b'],'t'] ])
	# 	else:
	# 		new_quilt.add_quilt_edge_constraints([ [top_edge_swatch,'l'] ])
	## if len(self.quilt_sequence)==0:
		# 	print "Error! Quilt already started. Can't seed it again."
		# 	return
		# first_quilt = self.setup_new_quilt()
		# first_quilt.add_quilt_edge_constraints([ [self.bottom_edge_swatch,'b'], [self.right_edge_swatch,'r'] ])
		# if left_edge_swatch is None:
		# 	left_edge_swatch = self.right_edge_swatch
		# if top_edge_swatch is None:
		# 	top_edge_swatch = self.bottom_edge_swatch
		# first_quilt.add_quilt_edge_constraints([ [left_edge_swatch,'l'], [self.top_edge_swatch,'t'] ])
		#
		# else:
		# 	first_quilt.add_quilt_edge_constraints( [ [left_edge_swatch, 'l']])
		# self.quilt_sequence += [new_quilt]
		# Add new minimum constraints so that we can start a new quilt sequence from scratch.
		# for i in range(self.n_columns):
		#
		#
		# self.bottom_edges = [bottom_edge]*self.n_columns
		# self.right_edges = [right_edge]
				
	# def add_quilt(self, left_edge=None, top_edge=None):
	# 	# Add a new quilt to the sequence.
	# 	# The right and bottom edges of the new quilt will automatically match the quilt sequence so far.
	# 	# If no new top or left edge constraints are given, then the bottom and right edges (respectively) will be duplicated.
	# 	quilt_n = self.n_quilts + 1
	# 	if len(self.right_edges)>quilt_n:
	# 		right_edge = self.right_edges[quilt_n]
	# 	else:
	# 		return "ERROR... tried to add a quilt but there was no right edge constraint."
	# 	if left_edge is None:
	# 		right_edge =
	#
	#
	# def duplicate_last_quilt(self):
	

p = Quilt(grid_size=(9,9), tile_size=(50,50))
# p.define_tile_designs(color_set = ["LightGray","MediumSeaGreen","Violet"])
p.define_tile_designs(color_set=["black","white"])
try_hard_to_make_tile(p, constraint_list=[ [["white"],"rb"], [["white","black"],"tl"] ])
p.write_quilt("quilts/quilt0")
for i in range(1,3):
	try_hard_to_make_tile(p, constraint_list=[ [["white"],"b"], [["white","black"],"tlr"] ])
	p.write_quilt("quilts/quilt"+str(i))

for i in range(3,6):
	try_hard_to_make_tile(p, constraint_list=[ [["white","black"],"tlrb"] ])
	p.write_quilt("quilts/quilt"+str(i))

p.define_tile_designs(color_set=["black","white","yellow"])
for i in range(6,9):
	try_hard_to_make_tile(p, constraint_list=[ [["white","black"],"tlrb"] ])
	p.write_quilt("quilts/quilt"+str(i))

i=9
try_hard_to_make_tile(p, constraint_list=[ [["white","black"],"rb"], [["white","yellow"],"lt"] ])
p.write_quilt("quilts/quilt"+str(i))

for i in range(10,12):
	try_hard_to_make_tile(p, constraint_list=[ [["white","black"],"b"], [["white","yellow"],"lrt"] ])
	p.write_quilt("quilts/quilt"+str(i))

for i in range(12,18):
	try_hard_to_make_tile(p, constraint_list=[ [["white","yellow"],"lrtb"] ])
	p.write_quilt("quilts/quilt"+str(i))

p.define_tile_designs(color_set=["yellow","white"])
for i in range(18,24):
	try_hard_to_make_tile(p, constraint_list=[ [["white","yellow"],"lrtb"] ])
	p.write_quilt("quilts/quilt"+str(i))


# Convert all the SVG files to PNGs

import subprocess
for i in range(24):
	cmd = ['/usr/local/bin/convert',"-density","600","'./quilts/quilt"+str(i)+".svg'","-resize","100%","'./quilts/quilt"+str(i)+".jpg'"]
	print " ".join(cmd)
	# subprocess.call(cmd)



p = Quilt(grid_size=(9,9), tile_size=(50,50))
p.define_tile_designs(color_set=[["yellow"],["white"]], tile_groups=["basic","1s","solids"])
for i in range(10,15):
	try_hard_to_make_tile(p, constraint_list=[ [["white","yellow"],"lrtb"] ])
	p.write_quilt("quilts/bubble"+str(i))

p = Quilt(grid_size=(9,9), tile_size=(50,50))
p.add_tile_designs(color_set=[["yellow","LightSkyBlue"],["white"]], tile_groups=["basic","1s","2s","3s","solids"])
p.add_tile_designs(color_set=[["yellow","LightSkyBlue"]], tile_groups=["basic","1s","2s","3s","solids"])
for i in range(20,25):
	try_hard_to_make_tile(p, constraint_list=[ [["white","yellow"],"lrtb"] ])
	p.write_quilt("quilts/bubble"+str(i))


p = Quilt(grid_size=(9,9), tile_size=(50,50))
p.add_tile_designs(color_set=[["LightSkyBlue","MidnightBlue"],["white"]], tile_groups=["basic","solids"])
for i in range(5,10):
	try_hard_to_make_tile(p, constraint_list=[ [["white","LightSkyBlue"],"lrtb"] ])
	p.write_quilt("quilts/wave"+str(i))

import subprocess
for i in range(5,10):
	cmd = ['/usr/local/bin/convert',"-density","600","'./quilts/wave"+str(i)+".svg'","-resize","100%","'./quilts/wave"+str(i)+".jpg'"]
	print " ".join(cmd)
	# subprocess.call(cmd)


