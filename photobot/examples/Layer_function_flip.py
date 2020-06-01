W,H = 1084, 798
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


def placeImage(path, x, y, maxsize, name):
    img1 = pb.resizeImage(path, maxsize)
    top = c.layer(img1, name=name)
    c.top.translate(x, y)
    w, h, = c.layers[ top ].bounds()
    return top, w, h


imsize = int((W-30)/2)
x, y = 10, 10
img1, w1, h1 = placeImage(img1path, x, y, imsize, "image1")
label("Original Image", x, y)

#
# flip horizontal
#
c.layers["image1"].duplicate()
c.top.name = "flip1"

x, y = w1+20, 10
c.top.translate( x, y)
c.top.flip( pb.HORIZONTAL )
label("Horizontal Flip", x, y)


#
# flip vertical
#

c.layers["image1"].duplicate()
c.top.name = "flip2"
x, y = 10 , h1 + 20
c.top.flip( pb.VERTICAL )
c.top.translate( x, y )
label("Vertical Flip", x, y)



#
# flip horizontal & vertical
#

# duplicate does not return top
c.layers["image1"].duplicate()
c.top.name = "flip3"

x, y = w1 + 20, h1 + 20
c.top.flip( pb.HORIZONTAL | pb.VERTICAL)
# c.top.flip( pb.VERTICAL )
c.top.translate( x, y)
label("Horizontal  and Vertical Flip", x, y)

# draw the result
c.draw(0, 0)


# this is just mean
# if you understand what it does, you're the next NodeBox maintainer...
canvas._grobs.reverse()



