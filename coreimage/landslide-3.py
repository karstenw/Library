kwdbg = False

size(1024, 768)


RATIO = WIDTH / HEIGHT

background( 0.333 )

import sys, os

import pprint
pp = pprint.pprint

# need a different name
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

# Import the Core Image library
try: 
    coreimage = ximport("coreimage")
except:
    print( "IMPORT MISSED!" )
    coreimage = ximport("__init__")
    reload(coreimage)


# import extensions if nodebox version < 1.9.18
try:
    imagefiles
except NameError:
    from nodeboxExtensions import *

# for topLayer, aspectRatio and label
from pbhelpers import *



# create the canvas
c = coreimage.canvas(WIDTH,HEIGHT)


# get all images from system "Desktop Pictures" folder
filetuples = imagefiles( "/Library/Desktop Pictures", False )

# filter out all 1 pix one color images by ignoring all files < 100k
tiles = []
for t in filetuples:
    path, filesize, lastmodified, mode, islink = t
    if filesize < 100000:
        continue
    tiles.append( path )

rnd.shuffle(tiles)
rnd.shuffle(tiles)
rnd.shuffle(tiles)



# CONFIGURATION

columns = 3
rows = 3

colwidth = WIDTH / columns
rowheight = HEIGHT / rows

positions = list(grid(columns, rows, colwidth, rowheight))


# base Image
if 1:
    img = tiles.pop()
    print( "base image:", img )
    l = c.layer(img)
    w, h = l.size()
    s = aspectRatio( (w,h), HEIGHT )
    l.scale(s, s)


for position in positions:
    x, y = position

    # top is the index of the image layer
    img = tiles.pop()
    print( "tile image:", img )
    l = c.layer(img)

    # scale the layer to row height
    scaleLayerToHeight( l, rowheight, pb=False )

    w, h = l.size()
    m = l.mask.layer_radial_gradient()
    if w > h:
        m.scale(w=w/h, h=1.0)
    else:
        m.scale(w=1.0, h=h/w)

    l.x = x
    l.y = y


c.draw(0, 0, helper=False)
