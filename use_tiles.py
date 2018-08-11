import tiles
import webcolors
import itertools
import pickle

# Defining a single tile, red on a white background, with two ellipses:
# 	(-1,0,1,1) = centred on (-1,0) with respect to the centre of the tile, and (x,y) dimension = (height,width) of tile.
#   (1,0,1,1)  = centred on (1,0) with same ellipse dimensions.
t = tiles.Tile(bg_color="white", fg_color="red", ellipses=[(-1,0,1,1), (1,0,1,1)], name="tmp", tile_size=(40,40))
# Tile filename will be "tmp_40"
t.create_tile_image()
# Inspect the edges to confirm that (top,right,bottom,left) edges are (white,red,white,red):
[webcolors.rgb_to_name(name) for name in t.ellipse_edge_colors()]

# Defining a single quilt:
q = tiles.Quilt(grid_size=(9,9), tile_groups=["basic","solids","2s"], fg_colors=["SeaGreen","black"], edge_command=[["white","black"],["white","black"],["white","black"],["white","black"]], verbose=False, name="seagreen")
flag = q.build_out_constrained_quilt_harder()
q.post_to_tumblr()


# 
#   Rough script for creating the blog
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

