import tiles
import webcolors
import itertools
import pickle
import numpy as np

# Defining a single tile, red on a white background, with two ellipses:
# 	(-1,0,1,1) = centred on (-1,0) with respect to the centre of the tile, and (x,y) dimension = (height,width) of tile.
#   (1,0,1,1)  = centred on (1,0) with same ellipse dimensions.
reload(tiles)
seed_quilt = tiles.Quilt(grid_size=(9,9), tile_groups=["basic","basic-3","1s"], fg_colors=["aqua","white","CornflowerBlue"], bg_colors=["white"], edge_command=[["CornflowerBlue","aqua"],["white","aqua"],["white","aqua"],["CornflowerBlue","aqua"]])
seq = tiles.QuiltSequence(seed_quilt, name="triples", n_columns=3)
seq.extend_sequence(reps=6)
seq.extend_sequence(reps=7,fg_colors=["aqua","CornFlowerBlue","navy"],bg_colors=["white","aqua","CornFlowerBlue","navy"], left_edge_swatch=["CornFlowerBlue","aqua"],top_edge_swatch=["CornFlowerBlue","aqua"])
seq.implement(overwrite=True)
seq.extend_sequence(reps=7,fg_colors=["aqua","CornFlowerBlue","navy"],bg_colors=["CornFlowerBlue","navy"])
seq.implement()


t = tiles.Tile(bg_color="white", ellipses=[(-1,0,1,1,webcolors.name_to_rgb("red")), (1,0,1,1,webcolors.name_to_rgb("red"))], name="tmp", tile_size=(70,70))
# (-1,1,2,2,webcolors.name_to_rgb("red"))
# Tile filename will be "tmp_40"
t.create_tile_image(overwrite=True)
q = tiles.Quilt(grid_size=(5,5), ellipses)


reload(tiles)
u = tiles.Tile(bg_color="white",ellipses=[(-1,-1,2,2,"red"), (1,1,2,2,"SeaGreen"), (0,1,.5,.5,"blue")], tile_size=[80,80], name="tmp")
u.create_tile_image(overwrite=True)
[webcolors.rgb_to_name(x) for x in u.edge_colors]
# Inspect the edges to confirm that (top,right,bottom,left) edges are (white,red,white,red):
[webcolors.rgb_to_name(name) for name in t.ellipse_edge_colors()]

# Defining a single quilt:
q = tiles.Quilt(grid_size=(9,9), tile_groups=["basic","solids","2s"], fg_colors=["SeaGreen","black"], edge_command=[["white","black"],["white","black"],["white","black"],["white","black"]], verbose=False, name="seagreen")
flag = q.build_out_constrained_quilt_harder()
q.post_to_tumblr()


# 
#   Script for creating the blog
# 
# Start with original tileset
reload(tiles)
seed_quilt = tiles.Quilt(grid_size=(9,9), tile_groups=["basic","1s"], fg_colors=["black","white"], bg_colors=["white","black"], edge_command=[["white","black"],["white"],["white"],["white","black"]])
seq = tiles.QuiltSequence(seed_quilt, name="master", n_columns=3)
seq.extend_sequence(reps=6)
seq.implement()
# Basic unit of time is ONE WEEK (7 posts).
# Week 2: sharp yellow
seq.extend_sequence(reps=7, fg_colors=["black","yellow","white"])
# Week 3: bubbly water
seq.extend_sequence(reps=7, fg_colors=["black","aqua"], tile_groups=["basic","1s","2s","3s"])
# Week 4: fading to aqua edges
seq.extend_sequence(reps=7, left_edge_swatch=["white","aqua"], top_edge_swatch=["white","aqua"])
seq.implement()
# Week 5: pure water
seq.extend_sequence(reps=7, tile_groups=["solids","basic"], fg_colors=["aqua","white"], bg_colors=["aqua","white"])
# Week 6: colourful water
seq.extend_sequence(reps=7, tile_groups=["solids","basic"], fg_colors=["aqua","white","CornflowerBlue"], bg_colors=["aqua","white"])
seq.implement()

for q in seq.qs:
	q.convert_quilt_to_img()
	q.post_to_tumblr()

# Save progress and reload same object later using pickles
pickle.dump(seq, open("master_blog_sequence.p", "wb"))

# To continue later, just reload the sequence:
reseq = pickle.load(open("master_blog_sequence.p", "rb"))

# Rewind to just after the yellows
reseq.quilt_sequence = reseq.quilt_sequence[:13]
reseq.name = 'master_magenta_insertion'
# Add a bunch of magentas
reseq.extend_sequence(reps=7, fg_colors=["black","magenta","white"],tile_groups=["basic","1s","2s"])
reseq.quilt_sequence = reseq.quilt_sequence[13:]
reseq.implement()
for q in reseq.quilt_sequence:
	q.convert_quilt_to_img()
	q.post_to_tumblr()

reseq.qs = reseq.quilt_sequence
pickle.dump(reseq, open("master_blog_sequence_magenta_insertion.p", "wb"))

# Writing second leg of sequence in stone:
seq = pickle.load(open("master_blog_sequence.p", "rb"))
# seq = tiles.QuiltSequence(reseq.qs[-1], name="dress_rehearsal", n_columns=3)
# seq.extend_sequence(reps=2)
seq.implement()
# Week 8: add navy
seq.extend_sequence(reps=7, tile_groups=["basic","1s","2s"], fg_colors=["aqua","CornflowerBlue","navy"], bg_colors=["white"])
seq.implement(max_iters=200)
seq.implement(max_iters=200)
# Week 9: make more densely navy using two-colour tiles
seq.extend_sequence(reps=7, tile_groups=["solids","basic","basic-3","1s"], fg_colors=["aqua","CornflowerBlue","navy"], bg_colors=["white"])
# seq.implement()
# Week 10: fade to navy edges:
seq.extend_sequence(reps=7, left_edge_swatch=["white","navy"], top_edge_swatch=["white","navy"])
# seq.implement()
# Week 11: no more cyan and cornflower, switch to navy and "Brown" (almost sienna red) on white
seq.extend_sequence(reps=7, left_edge_swatch=["Brown","navy"], top_edge_swatch=["Brown","navy"], fg_colors=["navy","Brown"], bg_colors=["navy","white"])
# Week 12: switch background from white to slate grey (almost green)
seq.extend_sequence(reps=7, fg_colors=["navy","Brown"], bg_colors=["DarkSlateGray"])
# Week 13: make navy the background instead of DarkSlateGray. Also, old-school tiles: basics and 1s!
seq.extend_sequence(reps=7, fg_colors=["Brown","DarkSlateGray"], bg_colors=["navy"], tile_groups=["basic","1s"])
# Week 14: Add LightGreen and make it the new edge color instead of Brown
seq.extend_sequence(reps=7, left_edge_swatch=["LightGreen","navy"], top_edge_swatch=["LightGreen","navy"], fg_colors=["LightGreen","Brown","DarkSlateGray"], bg_colors=["navy"], tile_groups=["basic","1s","basic-3","2s","3s"])
# Week 15: Eliminate Brown
seq.extend_sequence(reps=7, fg_colors=["LightGreen","DarkSlateGray"], bg_colors=["navy"], tile_groups=["basic","1s","2s","3s"])
# week 16: waves of LightGreen on navy
seq.extend_sequence(reps=7, tile_groups=["solids","basic"], fg_colors=["LightGreen","navy"], bg_colors=["LightGreen","navy"])
seq.implement()


for q in seq.qs[42:]:
	q.convert_quilt_to_img()
	q.post_to_tumblr()

# Save progress and reload same object later using pickles
pickle.dump(seq, open("master_blog_sequence_2.p", "wb"))




seq.implement(overwrite=True)
seq.extend_sequence(reps=7, tile_groups=["solids","basic","basic-3","1s"], fg_colors=["aqua","CornflowerBlue","navy","white"], bg_colors=["white"], left_edge_swatch=["white","navy"],top_edge_swatch=["white","navy"])
# seq.extend_sequence(reps=6, tile_groups=["solids","basic","1s"])
# seq.extend_sequence(reps=7, tile_groups=["solids","basic","2s","3s"], fg_colors=["aqua","CornflowerBlue"], bg_colors=["white","aqua"], left_edge_swatch=["aqua"], top_edge_swatch=["aqua","CornflowerBlue"])
seq.implement()





# Test out some new designs:

, top_edge_swatch=["aqua","CornflowerBlue"]

# Test out tile ideas on a temporary sequence:
tmp_seq = tiles.QuiltSequence(tiles.Quilt(grid_size=(9,9), tile_groups=["basic","solids"], fg_colors=["aqua","white"], bg_colors=["white","aqua"], edge_command=[["white","aqua"]]), name="test_seq", n_columns=3)
tmp_seq.extend_sequence(reps=6)

tmp_seq.extend_sequence(reps=7, fg_colors=["aqua","white","CornflowerBlue"], bg_colors=["aqua","white"], tile_groups=["solids","basic"])
tmp_seq.implement(overwrite=True)
tmp_seq.extend_sequence(reps=7, tile_groups=["solids","basic","1s","2s","3s"], fg_colors=["aqua","CornflowerBlue"])
tmp_seq.implement()

tmp_seq.extend_sequence(reps=7, fg_colors=["aqua","white","CornflowerBlue","MediumBlue"], bg_colors=["aqua","white"], tile_groups=["solids","basic","1s","2s"], left_edge_swatch=["white","CornflowerBlue"], top_edge_swatch=["white","CornflowerBlue"])
tmp_seq.extend_sequence(reps=7, fg_colors=["aqua","white","CornflowerBlue","MediumBlue"], bg_colors=["aqua","white"], tile_groups=["solids","basic","1s"], left_edge_swatch=["white","CornflowerBlue"], top_edge_swatch=["white","CornflowerBlue"])
tmp_seq.implement(overwrite=True)

