kwdbg = False

size(1000, 1000)

background( 0.333 )

# need a different name; random is taken
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

# import photobot
try:
    pb = ximport("photobot")
    pbh = ximport("pbhelpers")
except ImportError:
    pb = ximport("__init__")
    reload(pb)
from pbhelpers import *

# import extensions if nodebox version < 1.9.18
try:
    imagefiles
except NameError:
    from nodeboxExtensions import *


# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))


# get all images from system "Desktop Pictures" folder
filetuples = imagefiles( "/Library/Desktop Pictures", False )

# filetuples = imagefiles( "./+abi87/1_OLD", False )

# filter out all 1 pix one color images by ignoring all files < 100k
tiles = []
for t in filetuples:
    path, filesize, lastmodified, mode, islink = t
    if filesize < 100000:
        continue
    tiles.append( path )

# shuffle the images
rnd.shuffle(tiles)
rnd.shuffle(tiles)
rnd.shuffle(tiles)

#
# original image
#

#  create, scale and place the image
top = c.layer(tiles.pop(), name="image1")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
w1, h1, = c.layers[ top ].bounds()
c.layers[top].translate(10, 10)

label("Original", 10,10)

#
# flip horizontal
#
c.layers["image1"].duplicate()
top = topLayer(c)
c.layers[top].name = "flip1"

x, y = w1+20, 10
c.layers[top].translate( x, y)
c.layers[top].flip( pb.HORIZONTAL )
label("Horizontal Flip", x, y)


#
# flip vertical
#

c.layers["image1"].duplicate()
top = topLayer(c)
c.layers[top].name = "flip2"
x, y = 10 , h1 + 20
c.layers[top].flip( pb.VERTICAL )
c.layers[top].translate( x, y )
label("Vertical Flip", x, y)



#
# flip horizontal & vertical
#

# duplicate does not return top
c.layers["image1"].duplicate()
top = topLayer(c)
c.layers[top].name = "flip3"

x, y = w1 + 20, h1 + 20
c.layers[top].flip( pb.HORIZONTAL | pb.VERTICAL)
# c.layers[top].flip( pb.VERTICAL )
c.layers[top].translate( x, y)
label("Horizontal  and Vertical Flip", x, y)

# draw the result
c.draw(0, 0)


# this is just mean
# if you understand what it does, you're the next NodeBox maintainer...
canvas._grobs.reverse()

