# COLOR LIST FROM PIXELS

try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    # reload(colors)

kwlog = 0    
import imagewells

size(1440, 900)
background(None)

images = imagewells.loadImageWell(minsize=(400,300))
img = choice(images['allimages'])

n = 20

# A list of colors from image pixels.
# This requires the Core Image library to be installed.

sea = colors.list(img, n=n)

sea = list(set(sea))
n = len(sea)
w = round(WIDTH / n)
image(img, 0, w+5, width=WIDTH)

print( img )
# print( n )
print()

sea.sort()

x = 0
for clr in sea:
    fill(clr)
    rect(x, 0, w, w)
    x += w
