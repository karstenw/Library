# COLOR LIST FROM PIXELS

try:
    colors = ximport("colors")
except ImportError:
    colors = ximport("__init__")
    # reload(colors)
    

size(1200, 900)
background(None)


def findimage():
    while True:
        img = choice(list(imagefiles("/Library/Desktop Pictures")))
        x = imagesize(img)
        if x.width > 400:
            return img

n = 20

# A list of colors from image pixels.
# This requires the Core Image library to be installed.

img = findimage()

sea = colors.list(img, n=n)

sea = list(set(sea))
n = len(sea)
image(img, 0, 50, width=WIDTH)

print( img )
print( n )
print()

sea.sort()

w = WIDTH / n
x = 0
for clr in sea:
    fill(clr)
    rect(x, 0, w, 50)
    x += w
