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
