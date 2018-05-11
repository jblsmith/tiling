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
 

