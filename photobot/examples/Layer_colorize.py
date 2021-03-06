W,H = 532, 1050
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

# need a different name; random is taken
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

# import photobot
pb = ximport("photobot")
pbh = ximport("pbhelpers")
label = pbh.label

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


#
# Image 1
#

#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, 512, "Image 1", width=True)
label("Image 1", x, y)


# apply colorize
c.layers[top].colorize((240, 120, 0), (255, 255, 127))


# draw the result
c.draw(0, 0)
