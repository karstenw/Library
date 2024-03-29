import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

W, H = 542, 1050
fullwidth = int(W-20)
tilewidth = int((fullwidth-10) / 2.0)


# check for Nodebox
NB = True
try:
    _ctx
except(NameError):
    NB = False

if NB:
    size(W, H)
    pb = ximport("photobot")
else:
    WIDTH, HEIGHT = W, H
    import photobot as pb

import imagewells

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(8)

imagewell = imagewells.loadImageWell(resultfile="imagewell-files")
tiles = imagewell['landscape']
rnd.shuffle(tiles)


# pick 2 images
img1path = tiles.pop()
img2path = tiles.pop()

# create a gray canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (192, 192, 192) )

#
# Image 1
#

_, filename = os.path.split( img1path )

#  create, scale and place the image
x, y = 10, 10
img1, w1, h1 = pb.placeImage(c, img1path, x, y, WIDTH-20, "Image 1 Base")

c.top.autocontrast(cutoff=0)
pb.label(c, filename, x, y)

#
# Image 2
#
c.layers[img1].duplicate()

path=( (w1/2,0), (w1,int(h1*0.667)), (w1/2.0, h1), (0,h1*0.75),(0,h1/2) )
c.top.select( path )

x, y = 10, h1+20+10
c.top.translate( x, y)


# draw the result
c.draw(name="Layer_function_select")

