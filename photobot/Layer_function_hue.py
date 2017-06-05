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

# import extensions if nodebox version < 1.9.18
try:
    imagefiles
except NameError:
    from nodeboxExtensions import *

# for topLayer, aspectRatio and label
from pbhelpers import *
topLayer = pbh.topLayer
aspectRatio = pbh.aspectRatio
label = pbh.label

# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))


# get all images from system "Desktop Pictures" folder
filetuples = imagefiles( "/Library/Desktop Pictures", False )

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
# Image 1
#

img1path = tiles.pop()
img2path = tiles.pop()


#  create, scale and place the image
top = c.layer(img1path, name="image1")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
w1, h1, = c.layers[ top ].bounds()
c.layers[top].translate(10, 10)

label("Image 1", 10,10)

#
# Image 2
#
top = c.layer(img2path, name="image2")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
w1, h1, = c.layers[ top ].bounds()
top = topLayer(c)

x, y = w1+20, 10
c.layers[top].translate( x, y)
label("Image 2", x, y)


#
# Overlay Images 1 & 2
#

x, y = 10 , h1 + 20

top = c.layer(img1path, name="image3")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
c.layers[top].translate( x, y )

top = c.layer(img2path, name="image4")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
c.layers[top].translate( x, y )

c.layers[top].hue()
label("Hue Image1 over Image2", x, y)

#
# Overlay Images 2 & 1
#

x, y = w1+ 20 , h1 + 20

top = c.layer(img2path, name="image5")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
c.layers[top].translate( x, y )

top = c.layer(img1path, name="image6")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
c.layers[top].translate( x, y )

c.layers[top].hue()
label("Hue Image2 over Image1", x, y)


# draw the result
c.draw(0, 0)


# this is just mean
# if you understand what it does, you're the next NodeBox maintainer...
canvas._grobs.reverse()

