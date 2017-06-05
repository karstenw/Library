kwdbg = False

size(1000, 1200)

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


#  create, scale and place the image
top = c.layer(img1path, name="Image 1")
s = aspectRatio( c.layers[ top ].bounds(), 256 )
c.layers[top].scale(s, s)
w1, h1, = c.layers[ top ].bounds()
c.layers[top].translate(10, 10)
c.layers[top].opacity(100)
label("Image 1 Opacity: 100", 10,10)

#
# Image 2
#
c.layers[top].duplicate()
top = topLayer(c)
c.layers[top].name = "Image 2"
c.layers[top].opacity(80)

x, y = w1+20, 10
c.layers[top].translate( x, y)
label("Image 2 Opacity: 80", x, y)

#
# Image 3
#
c.layers[top].duplicate()
top = topLayer(c)
c.layers[top].name = "Image 3"
c.layers[top].opacity(60)

x, y = 10, h1 + 20
c.layers[top].translate( x, y)
label("Image 3 Opacity: 60", x, y)

#
# Image 4
#
c.layers[top].duplicate()
top = topLayer(c)
c.layers[top].name = "Image 4"
c.layers[top].opacity(40)

x, y = w1+20, h1 + 20
c.layers[top].translate( x, y)
label("Image 4 Opacity: 40", x, y)

#
# Image 5
#
c.layers[top].duplicate()
top = topLayer(c)
c.layers[top].name = "Image 5"
c.layers[top].opacity(40)

x, y = 10, 2*h1 + 30
c.layers[top].translate( x, y)
label("Image 3 Opacity: 40", x, y)

#
# Image 6
#
c.layers[top].duplicate()
top = topLayer(c)
c.layers[top].name = "Image 6"
c.layers[top].opacity(20)

x, y = w1+20, 2*h1 + 30
c.layers[top].translate( x, y)
label("Image 6 Opacity: 20", x, y)

#
# Image 7
#
c.layers[top].duplicate()
top = topLayer(c)
c.layers[top].name = "Image 7"
c.layers[top].opacity(150)

x, y = 10, 3*h1 + 40
c.layers[top].translate( x, y)
label("Image 7 Opacity: 150", x, y)

#
# Image 8
#
c.layers[top].duplicate()
top = topLayer(c)
c.layers[top].name = "Image 8"
c.layers[top].opacity(200)

x, y = w1 + 20, 3*h1 + 40
c.layers[top].translate( x, y)
label("Image 8 Opacity: 200", x, y)



# draw the result
c.draw(0, 0)


# this is just mean
# if you understand what it does, you're the next NodeBox maintainer...
canvas._grobs.reverse()

