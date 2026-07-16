# COLOR LIST FROM PIXELS

import pprint
pp=pprint.pprint
import imagewells

w,h = 1440,900
n = 20
from random import seed

# seed(1)

# find an image
images = imagewells.loadImageWell(minsize=( w, h ))
img = choice(images['allimages'])

# get imagesize 
W,H = imagesize( img, pixelsize=True )

colors = imagepalette( img, mask=224 )

# pp(colors)
sea = []
n = min( (n, len(colors) ) )

for i in range(n):
    col = colors[i]
    sea.append( color( *col ) )


tilesize = round( w / n )

# calculate image height + tiles + gap
if W > w:
    s = w / W
    h = (H * s) + tilesize + 5

size( w, h )
background(None)


image(img, 0, tilesize+5, width=WIDTH)

print( img )
print()

x = 0
for clr in sea:
    fill(clr)
    rect(x, 0, tilesize, tilesize)
    x += tilesize
