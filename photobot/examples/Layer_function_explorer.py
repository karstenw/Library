kwdbg = True

size(1024, 768)

background( 0.333 )

# need a different name; random is taken
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

# import photobot
try:
    pb = ximport("photobot")
except ImportError:
    pb = ximport("__init__")
    reload(pb)

# import extensions if nodebox version < 1.9.18
try:
    imagefiles
except NameError:
    from nodeboxExtensions import *

def topLayer( c ):
    # return top layer index
    return len(c.layers) -1

def aspectRatio(size, maxheight):
    """scale a (w,h) tuple to maxheight."""
    
    # NEEDED: scale to center square, not height
    
    w, h = size
    if h == maxheight:
        return 1.0
    elif maxheight == 0:
        return 1.0
    else:
        return float(maxheight) / h


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



#  create, scale and place the image
top = c.layer(tiles.pop(), name="image1")
img1 = top
w, h = c.layers[ top ].bounds()
s = aspectRatio( (w,h), 256 )
c.layers[top].scale(s, s)
w1, h1, = c.layers[ top ].bounds()
c.layers[top].translate(10, 10)

#  create, scale and place the image
top = c.layer(tiles.pop(), name="image2")
img2 = top
w, h = c.layers[ top ].bounds()
s = aspectRatio( (w,h), 256 )
c.layers[top].scale(s, s)
c.layers[top].translate(w1 + 20, 10)




# apply colorize
# c.layers[top].colorize((240, 120, 0), (255, 255, 127))


# draw the result
c.draw(0, 0)
