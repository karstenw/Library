# heavily inspired by https://www.nodebox.net/code/index.php/Landslide
size(0, 0)
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


import pbhelpers

try:
    imagefiles
except NameError:
    import helper_for_older_nodebox
    imagefiles = helper_for_older_nodebox.imagefiles

c = pb.canvas(int(WIDTH), int(HEIGHT))

tiles = list(imagefiles( "/Library/Desktop Pictures" ))


columns = 8
rows = 4

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
currlayer = c.layer(nextpictpath, name="0001")
c.layers[currlayer].scale(0.2,0.2)



def topLayer( c ):
    # return top layer index
    return len(c.layers) -1

for j in range(rows):
    for i in range(columns):

        # create image in canvas at 0,0
        nextpictpath = picts.pop()
        # print repr(nextpictpath)

        c.layer( nextpictpath )

        nlayers = len(c.layers)
        lastIndex = topLayer( c )
        c.layers[lastIndex].scale(0.2,0.2)

        # add contrast
        c.layers[ lastIndex ].contrast(1.1)

        # get current image bounds
        w, h = c.layers[ lastIndex ].bounds()

        # create gradient layer
        c.gradient(pb.LINEAR, w/2, h)

        nlayers = len(c.layers)
        lastIndex = topLayer( c )

        # layer + 4 flip
        c.layers[ lastIndex ].flip()

        # layer +4 translate half a pict right
        c.layers[ lastIndex ].translate(w/2, j*y_offset)

        # create gradient layer
        c.gradient(pb.LINEAR, w/2, h)
        lastIndex = topLayer( c )

        # merge gradient with 
        c.merge([ lastIndex - 1 , lastIndex ])
        lastIndex = topLayer( c )

        c.layers[ lastIndex ].brightness(1.4)
        
        c.layers[ lastIndex ].mask()
        lastIndex = topLayer( c )

        c.layers[ lastIndex ].translate(i*w/3, j*y_offset)

        if random() > 0.5:
            c.layers[ lastIndex ].flip()

        if random() > 0.5:
            c.layers[ lastIndex ].blur()

c.draw(10, 10)
