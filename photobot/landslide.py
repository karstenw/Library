
import sys, os

import pprint
pp = pprint.pprint

# need a different name
import random as rnd

background( 0.5 )

try:
    pb = ximport("photobot")
except ImportError:
    pb = ximport("__init__")
    reload(pb)


c = pb.canvas(800, 600)

folder = "./images"
#folder = "/Library/Desktop Pictures/wallstreet_wallpapers/Objects"

# finally an image folder that should exist on most macs
folder = "/Library/Desktop Pictures"

rawfiles = [f for f in os.listdir(folder)]
# rawfiles = files( folder + "/*.jpg" )

tiles = []
for t in rawfiles:
    if os.path.splitext(t)[1].lower() in [".jpg", ".png", ".tif", ".tiff", ".jpeg", ".gif"]:
        path = t
        if not path.startswith('/'):
            path = os.path.abspath(os.path.join(folder, t))
        tiles.append( path )
# pp(tiles)
# 
columns = 4
rows = 1

# 
y_offset = HEIGHT / (rows+1)

# x_offset = WIDTH / (columns * 2)

enoughTiles = len(tiles) > (columns*2*rows)

picts = []
for t in range(columns*rows*2):
    s = choice(tiles)
    picts.append(s)
    if enoughTiles:
        tiles.remove(s)

rnd.shuffle(picts)
nextpictpath = picts.pop()
c.layer(nextpictpath)
c.layers[1].scale(0.2,0.2)


def layerTop( c ):
    # return top layer index
    nlayers = len(c.layers)
    return nlayers -1


for j in range(rows):
    for i in range(columns):

        # create image in canvas at 0,0
        nextpictpath = picts.pop()
        print repr(nextpictpath)

        c.layer( nextpictpath )

        nlayers = len(c.layers)
        lastIndex = nlayers -1
        c.layers[lastIndex].scale(0.2,0.2)

        # add contrast
        c.layers[ lastIndex ].contrast(1.1)

        # get current image bounds
        w, h = c.layers[ lastIndex ].bounds()

        # create gradient layer
        c.gradient(pb.LINEAR, w/2, h)

        nlayers = len(c.layers)
        lastIndex = layerTop( c )

        # layer + 4 flip
        c.layers[ lastIndex ].flip()

        # layer +4 translate half a pict right
        c.layers[ lastIndex ].translate(w/2, j*y_offset)

        # create gradient layer
        c.gradient(pb.LINEAR, w/2, h)
        lastIndex = layerTop( c )

        # merge gradient with 
        c.merge([ lastIndex - 1 , lastIndex ])
        lastIndex = layerTop( c )

        c.layers[ lastIndex ].brightness(1.4)
        
        c.layers[ lastIndex ].mask()
        lastIndex = layerTop( c )

        c.layers[ lastIndex ].translate(i*w/3, j*y_offset)

        if 0: #random() > 0.5:
            c.layers[ lastIndex ].flip()

        if 0: #random() > 0.5:
            c.layers[ lastIndex ].blur()

c.draw(10, 10)
