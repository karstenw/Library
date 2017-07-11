W,H = 550, 1050
kwdbg = False

size(W, H)

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


img1path = tiles.pop()
img2path = tiles.pop()


def placeImage(path, x, y, maxsize, name):
    img1 = pb.resizeImage(path, maxsize)
    top = c.layer(img1, name=name)
    c.layers[top].translate(x, y)
    w, h, = c.layers[ top ].bounds()
    return top, w, h


#
# Image 1
#

#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = placeImage(img1path, x, y, 256, "Image 1")
label("Image 1", x, y)

#
# Image 2
#
x, y = w1+20, 10
top, w2, h2 = placeImage(img2path, x, y, 256, "Image 2")
label("Image 2", x, y)


#
# Screen Images 1 & 2
#

h = max(h1, h2)
x, y = 10 , h + 20

top, w3, h3 = placeImage(img1path, x, y, 522, "Image 3")
top, w4, h4 = placeImage(img2path, x, y, 522, "Image 4")

c.layers[top].screen()
label("Screen Image 1 over Image 2", x, y)


#
# Screen Images 2 & 1
#

h = max(h3, h4)
x, y = 10 , h + 20 + y

top, w4, h4 = placeImage(img2path, x, y, 522, "Image 5")
top, w3, h3 = placeImage(img1path, x, y, 522, "Image 6")

c.layers[top].screen()
label("Screen Image 2 over Image 1", x, y)

# draw the result
c.draw(0, 0)


# this is just mean
# if you understand what it does, you're the next NodeBox maintainer...
canvas._grobs.reverse()

