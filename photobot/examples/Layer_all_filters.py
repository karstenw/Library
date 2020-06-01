W,H = 820, 1050
# 
# Note:
#
# The examples may be easier to understand if you have LEO http://leoeditor.com installed
# and read them using the photobot.leo file
#
#
kwdbg = False

size(W, H)

background( 0.333 )

import os
# need a different name; random is taken
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

# import photobot
pb = ximport("photobot")
pbh = ximport("pbhelpers")
label = pbh.label

# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))



# build image name menu
filetuples = imagefiles( "/Library/Desktop Pictures", False )

images = {}
for f in filetuples:
    path = f[0]
    folder, filename = os.path.split( path )
    images[filename] = path

filenames = images.keys()
filenames.sort()


# build filter menu
filters = [
    'blur', 'contour', 'detail', 'edge_enhance',
    'edge_enhance_more', 'emboss', 'find_edges',
    'smooth', 'smooth_more']
filters.sort()
filters.insert(0, "None")

# globals
g_image = filenames[0]
g_filter = filters[0]

def imageselected(val, name):
    global g_image
    g_image = val
    path = images.get( val )

    print val
    pb.placeImage(c, path, 10, 50, WIDTH-20, "" )
    if g_filter == "blur":
        c.top.blur()
    elif g_filter == 'contour':
        c.top.contour()
    elif g_filter == 'detail':
        c.top.detail()
    elif g_filter == 'edge_enhance':
        c.top.edge_enhance()
    elif g_filter == 'edge_enhance_more':
        c.top.edge_enhance_more()
    elif g_filter == 'emboss':
        c.top.emboss()
    elif g_filter == 'find_edges':
        c.top.find_edges()
    elif g_filter == 'smooth':
        c.top.smooth()
    elif g_filter == 'smooth_more':
        c.top.smooth_more()
    c.draw(0,0)
    label(g_image + " " + g_filter, 10, 20)


def filterselected( menuitem, name ):
    global g_filter
    g_filter = menuitem
    imageselected( g_image, "" )


# new style menu var - defaults can now be set
var('Images', MENU, default= g_image, handler=imageselected, menuitems=filenames)
var('Filters', MENU, default= g_filter, handler=filterselected, menuitems=filters)

imageselected(g_image, "")
# draw the result
c.draw(0, 0)
