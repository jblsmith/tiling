
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


# # # 6. Create bot to generate output and post to Instagram

# Authenticate via OAuth
key_file_text = open("./keys.txt").readlines()
consumer_key, consumer_secret, oauth_token, oauth_secret = [line.split(", ")[1].strip('\n\'') for line in key_file_text]
import pytumblr
client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)

client.create_photo("randomtiles", state="draft", tags=["testing", "ok"],
                    data="./bubble23.jpg")

# "api.tumblr.com/v2/blog/randomtiles.tumblr.com/post"
