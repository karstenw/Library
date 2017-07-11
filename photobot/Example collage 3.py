W,H = 1280, 950
RATIO = W / H
import os
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



# CONFIGURATION

columns = 3
rows = 2

colwidth = int(WIDTH / columns)
rowheight = int(HEIGHT / rows)
maxsize = int(max(colwidth,rowheight)*1.2)

# print "colwidth/rowheight:", colwidth, rowheight

xgutter = colwidth * 0.0667
ygutter = rowheight * 0.0667
# print "xgutter/ygutter:", xgutter, ygutter

realwidth = colwidth - 1*xgutter
realheight = rowheight - 1*ygutter 

positions = list(grid(columns, rows, colwidth, rowheight))

randomblur = not kwdbg
paintoverlay = not kwdbg


#
# Base Image
#

#  create, scale and place the image
x, y = 0, 0
top, w, h = placeImage(img1path, x, y, W, "Image 1")


for position in positions:
    x, y = position


    # create image in canvas at 0,0
    p = tiles.pop()
    print p
    top, w, h = placeImage(p, 0, 0, maxsize, "Image %i,%i" % (x,y))

    # scale the layer to row height
    layer = c.layers[ top ]
    layer = scaleLayerToHeight( layer, rowheight )
    c.layers[ top ] = layer

    # uniform width
    #layer = c.layers[ top ]
    #layer = cropImageToRatioHorizontal( layer, RATIO )
    #c.layers[ top ] = layer

    # get the new image bounds - layer still valid
    w, h = layer.bounds()

    # add contrast - layer still valid
    layer.contrast(1.1)


    r = rnd.random()
    # 10%
    if 0 < r < 0.2:
        #print "20% LINEAR"
        # create gradient layer
        # top is now gradient index
        top = c.gradient(pb.LINEAR, w/2, h)
        c.layers[ top ].flip( pb.HORIZONTAL )

        # layer + 4 flip
        # c.layers[ top ].flip( pb.HORIZONTAL )

        # layer +4 translate half a pict right
        c.layers[ top ].translate(w/2, 0)

        # create gradient layer
        # top is now second gradient index
        top = c.gradient(pb.LINEAR, w/2, h)

        # merge both gradients; destroys top layer
        c.merge([ top-1 , top ])
    elif 0.2 <= r < 0.4:
        #print "20% SINE"
        top = c.gradient(pb.SINE, w, h)
        
    elif 0.4 <= r < 0.6:
        #print "20% RADIALCOSINE"
        top = c.gradient(pb.RADIALCOSINE, w, h)
        # c.layers[top].invert()
    elif 0.6 <= r < 0.8:
        #print "20% ROUNDRECT"
        # 25%
        top = c.gradient(pb.ROUNDRECT, w, h, "", radius=w/5.0, radius2=w/5.0)
    elif r >= 0.8:
        #print "20% QUAD"
        top = c.gradient(pb.QUAD, w, h, "", 0, 0)
            
    # print "After mask"
    top = c.topLayer()
    c.layers[ top ].brightness(1.4)
    # mask destroys top layer
    c.layers[ top ].mask()

    # top layer is now image with mask
    top = c.topLayer()

    destx = x - xgutter
    desty = y - ygutter
    # print "Image@", x, y
    # c.layers[ top ].translate(destx, desty)
    c.layers[ top ].translate(x, y)

    if randomblur:
        if rnd.random() > 0.5:
            #print "FLIP"
            c.layers[ top ].flip()

        if rnd.random() > 0.5:
            #print "BLUR"
            c.layers[ top ].blur()

if 0:
    # orange hue mask finish
    #print "Mr. Orange"
    top = c.fill((200,100,0))
    c.layers[top].opacity(30)
    c.layers[top].hue()

if paintoverlay:
    # paint overlay
    #print "VINCENT"
    top = c.layer( os.path.abspath("./paint.jpg") )
    w, h = c.layers[top].bounds()
    xs = WIDTH / float(w)
    ys = HEIGHT / float(h)
    s = max(xs,ys)
    c.layers[top].scale(s, s)
    c.layers[top].opacity(50)
    c.layers[top].overlay()



c.draw(0, 0)
