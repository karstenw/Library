# heavily inspired by https://www.nodebox.net/code/index.php/Landslide
kwdbg = False

if 0: #not kwdbg:
    size(0, 0)
    if not WIDTH and HEIGHT:
        size(1024, 768)
else:
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

def cropImageToRatioHorizontal( layer, ratio ):
    w, h = layer.bounds()
    neww = int( round( h*ratio) )
    d = int( neww / 2.0 )
    x,y,w,h = insetRect( (0,0,w,h), d, 0 )
    layer.img = layer.img.crop(box=(x,y,x+w,y+h))
    return layer
    

def insetRect( rectangle, horInset, vertInset):
    x, y, w, h = rectangle
    dh = horInset / 2.0
    dv = vertInset / 2.0
    return x+dh, y+dv, w-horInset, h-vertInset

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

# filter out all 1 pix one color images by ignoring all files < 100k
tiles = []
for t in filetuples:
    path, filesize, lastmodified, mode, islink = t
    if filesize < 100000:
        continue
    tiles.append( path )


rnd.shuffle(tiles)



# CONFIGURATION

columns = 3
rows = 2

randomblur = False
paintoverlay = False


# 
y_offset = HEIGHT / (rows)


# 
if 1:
    top = c.layer(tiles.pop())
    w, h = c.layers[ top ].bounds()
    s = aspectRatio( (w,h), HEIGHT )
    c.layers[1].scale(s, s)


def topLayer( c ):
    # return top layer index
    return len(c.layers) -1


for j in range(rows):
    colw = 0
    for i in range(columns):

        # create image in canvas at 0,0
        nextpictpath = tiles.pop()

        # top is the index of the image layer
        top = c.layer( nextpictpath )

        # get current image bounds
        w, h = c.layers[ top ].bounds()

        # calculate scale & apply
        s = aspectRatio( (w,h), y_offset)
        c.layers[ top ].scale(s, s)

        # uniform
        layer = c.layers[ top ]
        layer = cropImageToRatioHorizontal( layer, RATIO )
        c.layers[ top ]= layer

        # get the new image bounds
        w, h = c.layers[ top ].bounds()

        # add contrast
        c.layers[ top ].contrast(1.1)


        r = 0.4 #rnd.random()
        # 10%
        if r < 0.1:
            #print "COSINE/LINEAR"
            # create gradient layer
            # top is now gradient index
            top = c.gradient(pb.LINEAR, w/2, h)
            c.layers[ top ].flip( pb.HORIZONTAL )

            # layer + 4 flip
            # c.layers[ top ].flip( pb.HORIZONTAL )

            # layer +4 translate half a pict right
            c.layers[ top ].translate(w/2, j*y_offset)

            # create gradient layer
            # top is now second gradient index
            top = c.gradient(pb.LINEAR, w/2, h)
            # merge both gradients; destroys top layer
            c.merge([ top-1 , top ])
        elif 0.1 <= r < 0.5:
            #print "SINE"
            # create gradient layer
            # top i now gradient index
            top = c.gradient(pb.SINE, w, h)
            
        elif 0.6 <= r < 0.75:
            #print "RADIALCOSINE"
            # create gradient layer
            # top i now gradient index
            top = c.gradient(pb.RADIALCOSINE, w, h)
            c.layers[top].invert()
        else:
            #print "ROUNDRECT"
            # 25%
            top = c.gradient(pb.ROUNDRECT, w, h, radius=int(w/5.0))
            
        
        top = topLayer( c )

        c.layers[ top ].brightness(1.4)
        # mask destroys top layer
        c.layers[ top ].mask()

        # top layer is now image with mask
        top = topLayer( c )
        # c.layers[ top ].translate(colw+i*w/3, j*y_offset)
        c.layers[ top ].translate(colw+i*w, j*y_offset)
        # colw += i*w/2.0

        if randomblur:
            if rnd.random() > 0.5:
                c.layers[ top ].flip()

            if rnd.random() > 0.5:
                c.layers[ top ].blur()

if 1:
    # orange hue mask finish
    top = c.fill((200,100,0))
    c.layers[top].opacity(30)
    c.layers[top].hue()

if paintoverlay:
    # paint overlay
    top = c.layer( os.path.abspath("./paint.jpg") )
    w, h = c.layers[top].bounds()
    xs = WIDTH / float(w)
    ys = HEIGHT / float(h)
    s = max(xs,ys)
    c.layers[top].scale(s, s)
    c.layers[top].opacity(10)
    c.layers[top].overlay()



c.draw(0, 0)
