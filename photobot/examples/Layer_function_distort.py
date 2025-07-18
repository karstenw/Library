W,H = 800, 600
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


def placeImage(canvas, path, x, y, maxsize, name):
    img1 = pb.resizeImage(path, maxsize)
    top = canvas.layer(img1, name=name)
    canvas.layers[top].translate(x, y)
    w, h, = canvas.layers[ top ].bounds()
    return top, w, h

def transformimage(val, name):
    global x1,y1,x2,y2,x3,y3,x4,y420
    print( "transformimage(val, name):", val, name )
    # create the canvas
    c = pb.canvas(int(WIDTH), int(HEIGHT))
    c.fill(120, 120,120)
    _x1,_y1,_x2,_y2,_x3,_y3,_x4,_y4 = x1,y1,x2,y2,x3,y3,x4,y4
    x, y = 200, 200
    if name == 'x1':
        _x1 = val
    elif name == 'y1':
        _y1 = val
    elif name == 'x2':
        _x2 = val
    elif name == 'y2':
        _y2 = val
    elif name == 'x3':
        _x3 = val
    elif name == 'y3':
        _y3 = val
    elif name == 'x4':
        _x4 = val
    elif name == 'y4':
        _y4 = val
    
    top, w1, h1 = placeImage(c, img1path, x, y, 400, "Image 1")
    c.layers[top].distort(_x1,_y1,_x2,_y2,_x3,_y3,_x4,_y4)
    print( "x1,y1,x2,y2,x3,y3,x4,y4", _x1,_y1,_x2,_y2,_x3,_y3,_x4,_y4 )
    label("Image 1", x, y)
    c.draw(0, 0)
    canvas._grobs.reverse()
    print( "top:", top )

var("x1", NUMBER, 0, -200, 200, handler=transformimage)
var("y1", NUMBER, 0, -200, 200, handler=transformimage)
var("x2", NUMBER, 0, -200, 200, handler=transformimage)
var("y2", NUMBER, 0, -200, 200, handler=transformimage)
var("x3", NUMBER, 0, -200, 200, handler=transformimage)
var("y3", NUMBER, 200, -200, 200, handler=transformimage)
var("x4", NUMBER, 0, -200, 200, handler=transformimage)
var("y4", NUMBER, 0, -200, 200, handler=transformimage)


transformimage(1, "")

