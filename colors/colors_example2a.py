# COLOR LIST FROM PIXELS

try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    # reload(colors)

kwlog = 0    
import imagewells

w,h = 1440,900
n = 60



images = imagewells.loadImageWell(minsize=( w, h ))
img = choice(images['allimages'])

W,H = imagesize( img )



# A list of colors from image pixels.
# This requires the Core Image library to be installed.

sea = colors.list(img, n=n)

sea = list(set(sea))
n = len(sea)

tilesize = round( w / n )

# calculate image height + tiles + gap
if W > w:
    s = w / W
    h = (H * s) + tilesize + 5

size( w, h )
background(None)


image(img, 0, tilesize+5, width=WIDTH)

print( img )
# print( n )
print()

sea.sort()

x = 0
for clr in sea:
    fill(clr)
    rect(x, 0, tilesize, tilesize)
    x += tilesize
